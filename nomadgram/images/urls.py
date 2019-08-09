from django.urls import path
from . import views

app_name = "images"
urlpatterns = [
    path("", view=views.Feed.as_view(), name='feed'),
    path("<int:image_id>", view=views.ImageDetail.as_view(), name='image_detail'),
    path("<int:image_id>/likes/", view=views.LikeImage.as_view(), name='like_image'),
    path("<int:image_id>/unlikes/", view=views.UnLikeImage.as_view(), name='unlike_image'),
    path("<int:image_id>/comments/", view=views.CommentOnImage.as_view(), name='commet_image'),
    path("<int:image_id>/comments/<int:comment_id>/", view=views.ModerateComments.as_view(), name='moderate_commet'),
    path("comments/<int:comment_id>/", view=views.Comment.as_view(), name='comment'),
    path("search/", view=views.Search.as_view(), name='search'),
]

#url : 1.regular expression  2.view  3.name  

#     image/3/like/ 
# create the url and the view
# take the id from the url
# we want to field an image with this id
# we want to create a like for that image