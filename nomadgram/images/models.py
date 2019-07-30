from django.db import models
from nomadgram.users import models as user_models

# Create your models here.

class TimeStampedModel(models.Model):

    created_at = models.DateTimeField(auto_now_add=True)
    # 새로운  모델을 생성할 때 마다 자동으로 시간 입력 (auto_now_add = True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta: 
        abstract = True #abstract base class


class Image(TimeStampedModel):

    """ Image Model """

    file = models.ImageField()
    location = models.CharField(max_length = 140)
    caption = models.TextField()
    creator = models.ForeignKey(user_models.User, on_delete=models.PROTECT, null=True)

class Comment(TimeStampedModel):

    """ Comment Model """

    message = models.TextField()
    creator = models.ForeignKey(user_models.User, on_delete=models.PROTECT, null=True)
    image = models.ForeignKey(Image, on_delete=models.PROTECT, null=True)


class Like(TimeStampedModel):

    """ Like Model """

    creator = models.ForeignKey(user_models.User, on_delete=models.PROTECT, null=True)
    image = models.ForeignKey(Image, on_delete=models.PROTECT, null=True)
