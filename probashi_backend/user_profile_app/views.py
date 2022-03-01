from rest_framework import generics, status, views, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import permissions
from django.http import Http404

from auth_user_app.models import User
from .models import User_socialaccount_and_about, User_experience, User_education, User_idverification
from .serializers import UserProfileSkipPart1Serializer, UserProfileSkipPart2Serializer, UserSocialaccountAboutSerializer



class UserProfileSkipPart1(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self,userid):
        try:
            return User.objects.get(userid=userid)
        except User.DoesNotExist:
            raise Http404
    
    def put(self,request,userid):
        userid = self.get_object(userid)
        serializer = UserProfileSkipPart1Serializer(userid,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class UserProfileSkipPart2(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self,userid):
        try:
            return User.objects.get(pk=userid)
        except User.DoesNotExist:
            raise Http404
    
    def put(self,request,userid):
        userid = self.get_object(userid)
        serializer = UserProfileSkipPart2Serializer(userid,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class UserAboutSocialLink(views.APIView):
    def get_object(self,userid):
        try:
            return User_socialaccount_and_about.objects.get(userid=userid)
        except User_socialaccount_and_about.DoesNotExist:
            raise Http404

    def get(self,request,userid):
        userid = self.get_object(userid)
        serializer = UserSocialaccountAboutSerializer(userid)
        return Response(serializer.data)

    def put(self,request,userid):
        userid = self.get_object(userid)
        serializer = UserSocialaccountAboutSerializer(userid,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)




