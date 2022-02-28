from rest_framework import generics, status, views, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import permissions
from django.http import Http404

from auth_user_app.models import User
from .serializers import UserProfileSerializer




class DemoView(generics.GenericAPIView):

    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):

        return Response("user_profile_view",status=status.HTTP_204_NO_CONTENT)


#  problem : user_id exist kore previously. 
class UserProfile(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        user_profiledata = request.data
        serializer = UserProfileSerializer(data = user_profiledata)
        if serializer.is_valid():
            obj = serializer.save()
        context = {}
        context['user_fullname_passport'] = obj.user_fullname_passport

        return Response(context, status=status.HTTP_201_CREATED)

    def get(self, request):
        queryset = User.objects.all()
        serializer = UserProfileSerializer(queryset, many=True)
        return Response(serializer.data)

