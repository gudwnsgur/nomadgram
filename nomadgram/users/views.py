from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from . import serializers, models

# Url : path("explore/", view=views.ExploreUsers.as_view(), name="explore_users")
class ExploreUsers(APIView):

    def get(self, request, fomrat=None):
        last_five = models.User.objects.all().order_by('-date_joined')[:5]

        serializer = serializers.ListUserSerializer(last_five, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)



# Url : path("<int:user_id>/follow/", view=views.FollowUser.as_view(), name="follow_user")
class FollowUser(APIView):
    def post(self, request, user_id, format=None):
        user = request.user
        
        try : 
            user_to_follow = models.User.objects.get(id=user_id)
        except models.User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        user.following.add(user_to_follow)
        user_to_follow.followers.add(user)

        return Response(status=status.HTTP_200_OK)

# Url : path("<int:user_id>/unfollow/", view=views.UnFollowUser.as_view(), name="unfollow_user")
class UnFollowUser(APIView):
    def put(self, request, user_id, format=None):
        user = request.user
        
        try: 
            user_to_follow = models.User.objects.get(id=user_id)
        except models.User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        user.following.remove(user_to_follow)
        user_to_follow.followers.remove(user)

        return Response(status=status.HTTP_200_OK)


# Url : path("<username>/", view=views.UserProfile.as_view(), name="user_profile" )
class UserProfile(APIView):
    def get(self, request, username, format=None):

        try:
            found_user = models.User.objects.get(username=username)
        except models.User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        serializer = serializers.UserProfileSerializer(found_user) 
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    

class UserFollowers(APIView):
    def get(self, request, username, format=None):

        try:
            found_user = models.User.objects.get(username=username)
        except models.User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        user_followers = found_user.followers.all()

        serializer = serializers.ListUserSerializer(user_followers, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

class UserFollowing(APIView):
    def get(self, request, username, format=None):

        try:
            found_user = models.User.objects.get(username=username)
        except models.User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        user_following = found_user.following.all()

        serializer = serializers.ListUserSerializer(user_following, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)