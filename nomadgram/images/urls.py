from django.urls import path
from . import views

app_name = "images"
urlpatterns = [
    path("all/", view=views.ListAllImages.as_view(), name="all_imaes"),
    path("comments/", view=views.ListAllComments.as_view(), name="all_comment"),
    path("likes/", view=views.ListAllLikes.as_view(), name="all_likes"),
]

#url : 1.regular expression  2.view  3.name  