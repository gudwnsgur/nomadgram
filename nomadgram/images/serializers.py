# translation between javascript and python
# django rest framework 의 serializer가 python object <--> json object 변경해줌

from rest_framework import serializers
from . import models

class CommentSerializer(serializers.ModelSerializer):

    # image = ImageSerializer()    image field inside of Comment model

    class Meta:
        model = models.Comment
        fields = '__all__'

class LikeSerializer(serializers.ModelSerializer):

    # image = ImageSerializer()    image field inside of Like model

    class Meta:
        model = models.Like
        fields = '__all__'        


class ImageSerializer(serializers.ModelSerializer):

    comments = CommentSerializer(many=True)
    likes = LikeSerializer(many=True)

    class Meta:
        model = models.Image
        fields =  (
            'id',
            'file',
            'location',
            'caption',
            'comments',
            'likes'
        )
