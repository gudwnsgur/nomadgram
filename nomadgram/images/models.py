from django.db import models
from taggit.managers import TaggableManager
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
    creator = models.ForeignKey(user_models.User, on_delete=models.PROTECT, null=True, related_name='images')
    #creator : 생성자
    tags = TaggableManager()


    #property : field of a model that dosen't go DB but still is inside of a model
    @property
    def like_count(self):
        return self.likes.all().count()

    @property
    def comment_count(self):
        return self.comments.all().count()

    def __str__(self):
        return '{} - {}'.format(self.location, self.caption)

    class Meta:
        ordering = ['-created_at']

class Comment(TimeStampedModel):

    """ Comment Model """

    message = models.TextField()
    creator = models.ForeignKey(user_models.User, on_delete=models.PROTECT, null=True)
    image = models.ForeignKey(Image, on_delete=models.PROTECT, null=True, related_name='comments')
    
    def __str__(self):
        return self.message


class Like(TimeStampedModel):

    """ Like Model """

    creator = models.ForeignKey(user_models.User, on_delete=models.PROTECT, null=True)
    image = models.ForeignKey(Image, on_delete=models.PROTECT, null=True, related_name='likes')

    def __str__(self):
        return ' User : {} - Image Caption : {}'.format(self.creator.username, self.image.caption)