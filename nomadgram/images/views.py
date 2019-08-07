from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from . import serializers, models
from nomadgram.notifications import views as notification_views

# Url : path("", view=views.Feed.as_view(), name='feed')
class Feed(APIView):
    def get(self, request, format=None):
        
        user = request.user

        following_users = user.following.all()

        image_list = []

        for following_user in following_users:
            user_images = following_user.images.all()[:2]

            for image in user_images:

                image_list.append(image)

        sorted_list = sorted(image_list, key=lambda image:image.created_at, reverse=True)
        
        serializer = serializers.ImageSerializer(sorted_list, many=True)

        return Response(serializer.data)        



# Url : path("<int:image_id>/likes/", view=views.LikeImage.as_view(), name='like_image')
class LikeImage(APIView):
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