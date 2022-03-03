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
                            UserExperienceUpdatSerializer, UserEducationCreateSerializer,
                            UserIdVerificationCreateSerializer)



class UserProfileSkipPart1(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get_user(self,userid):
        try:
            return User.objects.get(userid=userid)
        except User.DoesNotExist:
            raise Http404
    
    def put(self,request,userid):
        userid = self.get_user(userid)
        serializer = UserProfileSkipPart1Serializer(userid,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class UserProfileSkipPart2(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get_user(self,userid):
        try:
            return User.objects.get(pk=userid)
        except User.DoesNotExist:
            raise Http404
    
    def put(self,request,userid):
        userid = self.get_user(userid)
        serializer = UserProfileSkipPart2Serializer(userid,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class UserEditProfile(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get_user(self,userid):
        try:
            return User.objects.get(userid__exact=userid)
        except User.DoesNotExist:
            raise Http404

    def get(self,request,userid):
        userid = self.get_user(userid)
        serializer = UserEditPrifileSerializer(userid)
        return Response(serializer.data)

    def put(self,request,userid):
        userid = self.get_user(userid)
        serializer = UserEditPrifileSerializer(userid,data=request.data)
        
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class UserAboutSocialLinkCreate(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)


    # def get_user(self,userid):
    #     try:
    #         return User_socialaccount_and_about.objects.get(userid__exact=userid)
    #     except User.DoesNotExist:
    #         raise Http404



    # def get(self,request, userid):
    #     userid = self.get_user(userid)
    #     serializer = UserSocialaccountAboutCreateSerializer(userid, many=True)
    #     return Response(serializer.data)

    def post(self,request):
        serializer = UserSocialaccountAboutCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

"""
class UserAboutSocialLinkUpdate(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)
    
    def get_user(self,userid):
        try:
            return User_socialaccount_and_about.objects.get(userid__exact=userid)
        except User_socialaccount_and_about.DoesNotExist:
            raise Http404

    def get(self,request,userid):
        userid = self.get_user(userid)
        serializer = UserSocialaccountAboutUpdatSerializer(userid)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)

    def put(self,request,userid):
        userid = self.get_user(userid)
        serializer = UserSocialaccountAboutUpdatSerializer(userid,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

"""

class UserExperienceCreate(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self,request):
        serializer = UserExperienceCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


# class UserExperienceUpdate(views.APIView):
#     permission_classes = (permissions.IsAuthenticated,)


#     def get_user(self,userid):
#         try:
#             return User_experience.objects.filter(userid__exact=userid)
#         except User_socialaccount_and_about.DoesNotExist:
#             raise Http404
    
#     def get_experience(self,id):
#         try:
#             return User_experience.objects.filter(id=id)
#         except User_socialaccount_and_about.DoesNotExist:
#             raise Http404

#     def get(self,request,userid):
#         userid = self.get_user(userid)
#         serializer = UserExperienceUpdatSerializer(userid, many=True)
#         return Response(serializer.data)

#     def put(self,request,userid):
#         userid = self.get_user(userid)
#         experienceid = self.get_experience(request.data['id'])
#         print('experienced:::::',experienceid)

#         print('request.dat:::::',request.data)

#         serializer = UserExperienceUpdatSerializer(experienceid,data=request.data)
#         # lookup_field = "id"

#         if serializer.is_valid():
#             # serializer.save()
#             print('serializer.data::::::',serializer.data)
#             return Response(serializer.data)
#         return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)






class UserEducationCreate(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self,request):
        serializer = UserEducationCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)



class UserIdVerificationCreate(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self,request):
        serializer = UserIdVerificationCreateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)














