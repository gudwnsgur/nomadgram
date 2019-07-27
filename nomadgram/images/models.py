from django.db import models

# Create your models here.

class TimeStampedModel(models.Model):

    created_at = models.DateTimeField(auto_now_add=True)
    # 새로운  모델을 생성할 때 마다 자동으로 시간 입력 (auto_now_add = True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta: 
        abstract = True #abstract base class


class Image(TimeStampedModel):

    file = models.ImageField()
    location = models.CharField(max_length = 140)
    caption = models.TextField()



class Comment(TimeStampedModel):

    message = models.TextField()