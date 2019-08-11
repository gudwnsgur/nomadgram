from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from . import serializers, models
from nomadgram.users import models as user_models
from nomadgram.users import serializers as user_serializers
from nomadgram.notifications import views as notification_views

# Url : path("", view=views.Images.as_view(), name='images')
class Images(APIView):
    def get(self, request, format=None):
        
        user = request.user
        following_users = user.following.all()

        image_list = []

        for following_user in following_users:
            user_images = following_user.images.all()[:2]

            for image in user_images:

                image_list.append(image)

        my_images = user.images.all()[:2]
        for image in my_images:
            image_list.append(image)

        sorted_list = sorted(image_list, key=lambda image:image.created_at, reverse=True)
        
        serializer = serializers.ImageSerializer(sorted_list, many=True)

        return Response(serializer.data)       

    def post(self, request, format=None):
        user = request.user
        serializer = serializers.InputImageSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save(creator=user)
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

# Url : path("<int:image_id>/likes/", view=views.LikeImage.as_view(), name='like_image')
class LikeImage(APIView):

    def get(self, request, image_id, format=None):
        likes = models.Like.objects.filter(image__id=image_id)

        like_creators_ids = likes.values('creator_id')

        users = user_models.User.objects.filter(id__in=like_creators_ids)

        serializer = user_serializers.ListUserSerializer(users, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


    def post(self, request, image_id, format=None):         
        # if something changes on the DataBase, the request should be post
        user = request.user

        try :
            found_image = models.Image.objects.get(id=image_id)   
            # 필터링해서 model을 읽고자 할 때 objects 사용
        except models.Image.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        try:
            models.Like.objects.get(
                creator = user,
                image = found_image
            )
            return Response(status=status.HTTP_304_NOT_MODIFIED)

        except models.Like.DoesNotExist:
            new_like = models.Like.objects.create(
                creator = user,
                image = found_image
            )   
            new_like.save()
            notification_views.create_notification(
               user, found_image.creator, 'like', found_image)

            return Response(status=status.HTTP_201_CREATED)



# Url : path("<int:image_id>/unlikes/", view=views.UnLikeImage.as_view(), name='unlike_image')
class UnLikeImage(APIView):
    def delete(self, request, image_id, format=None):

        user = request.user
        try:
            found_image = models.Image.objects.get(id=image_id)
        except models.Image.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        try:
            preexisiting_like = models.Like.objects.get(
                creator = user,
                image = found_image
            )
            preexisiting_like.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except models.Like.DoesNotExist:
            return Response(status=status.HTTP_304_NOT_MODIFIED)


# Url : path("<int:image_id>/comments/", view=views.CommentOnImage.as_view(), name='commet_image')
class CommentOnImage(APIView):

    def post(self, request, image_id, format=None):
        user = request.user

        try :
            found_image = models.Image.objects.get(id=image_id)  
        except models.Image.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = serializers.CommentSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(creator=user, image=found_image)
            notification_views.create_notification(
                user, found_image.creator, 'comment', found_image, serializer.data['message'])

        
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else : 
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# Url : path("comments/<int:comment_id>/", view=views.Comment.as_view(), name='comment')
class Comment(APIView):
    def delete(self, request, comment_id, format=None):
        
        user = request.user

        try:
            comment = models.Comment.objects.get(id=comment_id, creator=user)
            comment.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except models.Comment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

class Search(APIView):
    def get(self, request, formnat=None):
        hashtags = request.query_params.get('hashtags', None)
        print(hashtags)
        if hashtags is not None:
            hashtags = hashtags.split(",")
        
            images = models.Image.objects.filter(tags__name__in=hashtags).distinct()
            serializer = serializers.CountImageSerializer(images, many=True)

            return Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

# path("<int:image_id>/comments/<int:comment_id>/", view=views.ModerateComments.as_view(), name='moderate_commet')
class ModerateComments(APIView):
    def delete(self, request, image_id, comment_id, format=None):
        user = request.user

        try:
            comment_to_delete = models.Comment.objects.get(
                id=comment_id, image__id = image_id, image__creator=user )
            comment_to_delete.delete()
        except models.Image.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        return Response(status=status.HTTP_204_NO_CONTENT)



# path("<int:image_id>", view=views.ImageDetail.as_view(), name='image_detail')
class ImageDetail(APIView): # only can get my image

    def find_own_image(self, image_id, user):
        try: 
            image = models.Image.objects.get(id=image_id, creator=user)
            return image
        except models.Image.DoesNotExist:
            return None

    def get(self, request, image_id, format=None):
        try: 
            image = models.Image.objects.get(id=image_id)
        except models.Image.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = serializers.ImageSerializer(image)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


    def put(self, request, image_id, format=None):
        user = request.user

        image = self.find_own_image(image_id, user)
        
        if image is None:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        serializer = serializers.InputImageSerializers(image, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save(creator=user)
            return Response(data=serializer.data, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, image_id, format=None):
        user = request.user
        image = self.find_own_image(image_id, user)
        
        if image is None:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        image.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
