from rest_framework import generics, status, views, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import permissions
from django.http import Http404

from auth_user_app.models import User
from .models import User_socialaccount_and_about, User_experience, User_education, User_idverification
from .serializers import (UserProfileSkipPart1Serializer, UserProfileSkipPart2Serializer,
                            UserEditPrifileSerializer, UserSocialaccountAboutCreateSerializer,
                            UserSocialaccountAboutUpdatSerializer, UserExperienceCreateSerializer,
                            UserExperienceUpdatSerializer)



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


class UserEditProfile(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self,userid):
        try:
            return User.objects.get(userid__exact=userid)
        except User.DoesNotExist:
            raise Http404

    def get(self,request,userid):
        userid = self.get_object(userid)
        serializer = UserEditPrifileSerializer(userid)
        return Response(serializer.data)

    def put(self,request,userid):
        userid = self.get_object(userid)
        serializer = UserEditPrifileSerializer(userid,data=request.data)
        
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class UserAboutSocialLinkCreate(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self,request):
        userid = User_socialaccount_and_about.objects.all()
        serializer = UserSocialaccountAboutCreateSerializer(userid, many=True)
        return Response(serializer.data)

    def post(self,request):
        serializer = UserSocialaccountAboutCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class UserAboutSocialLinkUpdate(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)
    
    def get_object(self,userid):
        try:
            return User_socialaccount_and_about.objects.get(userid=userid)
        except User_socialaccount_and_about.DoesNotExist:
            raise Http404

    def get(self,request,userid):
        userid = self.get_object(userid)
        serializer = UserSocialaccountAboutUpdatSerializer(userid)
        return Response(serializer.data)

    def put(self,request,userid):
        userid = self.get_object(userid)
        serializer = UserSocialaccountAboutUpdatSerializer(userid,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class UserExperienceCreate(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)


    def get(self,request):
        userid = User_experience.objects.all()
        serializer = UserExperienceCreateSerializer(userid, many=True)
        return Response(serializer.data)

    def post(self,request):
        serializer = UserExperienceCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class UserExperienceUpdate(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)


    def get_object(self,userid):
        try:
            return User_experience.objects.get(userid=userid)
        except User_socialaccount_and_about.DoesNotExist:
            raise Http404

    def get(self,request,userid):
        userid = self.get_object(userid)
        serializer = UserExperienceUpdatSerializer(userid, many=True)
        return Response(serializer.data)

    def put(self,request,userid):
        userid = self.get_object(userid)
        serializer = UserExperienceUpdatSerializer(userid,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)







