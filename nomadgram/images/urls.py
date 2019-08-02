from django.urls import path
from . import views

app_name = "images"
urlpatterns = [
    path("", view=views.Feed.as_view(), name='feed'),
    path("<int:image_id>/like/", view=views.LikeImage.as_view(), name='like_image'),
]

#url : 1.regular expression  2.view  3.name  

#     image/3/like/ 
# create the url and the view
# take the id from the url
# we want to field an image with this id
# we want to create a like for that image

