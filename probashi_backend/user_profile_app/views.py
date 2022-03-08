from lib2to3.pgen2.token import EQUAL
from rest_framework import generics, status, views, permissions, viewsets
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
                            UserIdVerificationCreateSerializer,
                            UserProfileViewSerializer,UserIDverificationSerializer)
from rest_framework.decorators import action



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




# class UserProfileView(generics.ListAPIView):
#     permission_classes = [permissions.IsAuthenticated,]
#     serializer_class = UserProfileViewSerializer

#     def get_queryset(self):
#             user = self.request.user
#             # user_id = User.objects.all().filter(user_email=user).values('userid')
#             # user_id = user_id[0].get('userid')
#             # return(User.objects.filter(userid=user_id))
#             return User.objects.filter(user_email=user)

class UserProfileView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated,]
    serializer_class = UserProfileViewSerializer

    def get_queryset(self):
            user = self.request.user
            # user_id = User.objects.all().filter(user_email=user).values('userid')
            # user_id = user_id[0].get('userid')
            # return(User.objects.filter(userid=user_id))

            return User.objects.filter(user_email=user)

    def list(self, request):
        # Note the use of `get_queryset()` instead of `self.queryset`
        queryset = self.get_queryset()
        serializer = UserProfileViewSerializer(queryset, many=True)
        # serializerdata = serializer.data
        '''
        [OrderedDict([('userid', '0306144709829726'), ('user_fullname', 'demodemo100'), 
        ('user_photopath', '/upload/user/profile_picture/0d3866b3-cfc5-45bb-83f9-7585975d413e.png'), 
        ('is_consultant', False), ('user_industry', None), ('user_geolocation', 'Amazon, africa'), 
        ('user_created_at', '2022-03-06T14:47:10.044244+06:00'), ('user_interested_area', None), ('user_goal', None), 
        ('user_industry_experienceyear', None), ('user_areaof_experience', None), ('user_socialaboutdata', None), 
        ('user_experiencedata', []), ('user_educationdata', []), ('user_idverificationdata', [])])]
        
        '''

        # print('serializer data::::::',serializerdata)
        # print(serializerdata[0]['user_socialaboutdata'])



        if serializer.data[0]['user_socialaboutdata'] != None and serializer.data[0]['user_experiencedata'] != [] and \
                serializer.data[0]['user_educationdata'] != [] and serializer.data[0]['user_idverificationdata'] != [] : 
            user = self.request.user
            User.objects.filter(user_email=user).update(is_consultant=True)    

        complete_profile_persentage = 20
        if serializer.data[0]['user_socialaboutdata'] != None:
            complete_profile_persentage += 20
        if serializer.data[0]['user_experiencedata'] != []:
            complete_profile_persentage += 20
        if serializer.data[0]['user_educationdata'] != []:
            complete_profile_persentage += 20
        if serializer.data[0]['user_idverificationdata'] != []:
            complete_profile_persentage += 20
        serializer.data[0]['profile_complete_percentage'] = complete_profile_persentage



        if serializer.data[0]['user_socialaboutdata'] == None:
            serializer.data[0]['user_socialaboutdata'] = {
            "user_about": "null",
            "user_fbaccount": "null",
            "user_twitteraccount": "null",
            "user_instagramaccount": "null",
            "user_linkedinaccount": "null",
            "user_website": "null",
            "user_whatsapp_account": "null",
            "user_whatsapp_visibility": "null",
            "user_viber_account": "null",
            "user_immo_account": "null"
            }

        if serializer.data[0]['user_experiencedata'] == []:
            serializer.data[0]['user_experiencedata'] = {
                "id": "null",
                "user_designation": "null",
                "user_companyname": "null",
                "user_responsibilities": "null",
                "userexperience_startdate": "null",
                "userexperience_enddate": "null",
                "userid": "null"
            }

        if serializer.data[0]['user_educationdata'] == []:
            serializer.data[0]['user_educationdata'] = {
                "id": "null",
                "user_edu_degree": "null",
                "user_edu_institutename": "null",
                "user_edu_startdate": "null",
                "user_edu_enddate": "null",
                "userid": "null"
            }

        if serializer.data[0]['user_idverificationdata'] == []:
            serializer.data[0]['user_idverificationdata'] = {
                "id": "null",
                "is_user_permanent_resident": "null",
                "user_verify_id_type": "null",
                "user_verify_passportphoto_path": "null",
                "userid": "null"
            }

        # if User.objects.filter(is_consultant=True):
            # 1st complete consultance API then add Consultancy serilizer to nested user serializer
            #  then modifi to give active consultancy on User profile

        return Response(serializer.data)















