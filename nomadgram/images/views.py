from rest_framework.views import APIView
from rest_framework.response import Response
from . import models
from . import serializers

class ListAllImages(APIView):

    def get(self, request, format=None):    # format will be json

        all_images = models.Image.objects.all() # get all objects kind of images in models
        # variable that all of image object on DB

        serializer = serializers.ImageSerializer(all_images, many=True)
        return Response(data=serializer.data)   # end of function


class ListAllComments(APIView):
    def get(self, request, format=None): 
        all_comments = models.Comment.objects.all() # get all objects kind of comments in models

        serializer = serializers.CommentSerializer(all_comments, many=True)
        return Response(data=serializer.data)


class ListAllLikes(APIView):
    def get(self, request, format=None):
        all_likes = models.Like.objects.all() # get all likes in models

        serializer = serializers.LikeSerializer(all_likes, many=True)
        return Response(data=serializer.data)