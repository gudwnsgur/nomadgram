# translation between javascript and python
from rest_framework import serializers
from . import models

class ImageSerializer(serializers.Serializer):

    class Meta:
        model = models.Image
        fields = '__all__'


class CommentSerializer(serializers.Serializer):

    class Meta:
        model = models.Comment
        fields = '__all__'

class LikeSerializer(serializers.Serializer):

    class Meta:
        model = models.Like
        fiels = '__all__'        
