from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from . import serializers, models


class ExploreUsers(APIView):

    def get(self, request, fomrat=None):
        last_five = models.User.objects.all().order_by('-date_joined')[:5]

        serializer = serializers.ExploreUserSerializer(last_five, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)