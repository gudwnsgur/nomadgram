# translation between javascript and python
# django rest framework 의 serializer가 python object <--> json object 변경해줌

from rest_framework import serializers
from . import models
from nomadgram.users import models as user_models

class SmallImageSerializer(serializers.ModelSerializer):
    # Used for the notifications
    class Meta:
        model = models.Image
        fields = (   
            'file',
        )

class CountImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Image
        fields = (
            'id',
            'file',
            'comment_count',
            'like_count'
        )

class FeedUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = user_models.User
        fields = (
            'username',
            'profile_image'
        )


class CommentSerializer(serializers.ModelSerializer):

    # image = ImageSerializer()    image field inside of Comment model

    creator = FeedUserSerializer(read_only=True)
    class Meta:
        model = models.Comment
        fields = (
            'id',
            'message',
            'creator'
        )

class LikeSerializer(serializers.ModelSerializer):

    # image = ImageSerializer()    image field inside of Like model

    class Meta:
        model = models.Like
        fields = '__all__'        

class ImageSerializer(serializers.ModelSerializer):

    comments = CommentSerializer(many=True)
    creator = FeedUserSerializer()

    class Meta:
        model = models.Image
        fields =  (
            'id',
            'file',
            'location',
            'caption',
            'comments',
            'like_count',
            'creator',
            'created_at'
        )

class InputImageSerializers(serializers.ModelSerializer):
    class Meta:
        model = models.Image
        fields = (
            'file',
            'location',
            'caption'
        )