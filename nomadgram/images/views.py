from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from . import serializers, models

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
        
        
# post의 문제점 : browser에 새로고침하면서 사용할 수 없다.

class LikeImage(APIView):
    def post(self, request, image_id, format=None):         # if something changes on the DataBase, the request should be post
        
        user = request.user

        try :
            found_image = models.Image.objects.get(id=image_id)   # 필터링해서 model을 읽고자 할 때 objects 사용
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
            new_like = models.Like.objects.create(
                creator = user,
                image = found_image
            )   
        new_like.save()
        return Response(status=status.HTTP_201_CREATED)


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

            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else : 
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
class Comment(APIView):
    def delete(self, request, comment_id, format=None):
        
        user = request.user

        try:
            comment = models.Comment.objects.get(id=comment_id, creator=user)
            comment.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except models.Comment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)