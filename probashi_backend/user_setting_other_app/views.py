from multiprocessing import context
from rest_framework import generics, status, views, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import permissions
from django.http import Http404
from .models import StaticSettingData,Notification
from auth_user_app.models import User
from .serializers import (UserIndustryDataSerializer,
                    UserAreaOfExperienceDataSerializer,
                    UserInterestedAreaDataSerializer,
                    UserGoalDataSerializer,
                    ConsultancyServiceCategoryDataSerializer,
                    CreateOtherRowsInStatictableSerializer,
                    BlogTagDataSerializers,
                    UserEducationDataSerializer,
                    FacingtroubleSerializer,
                    FaqSerializer, privacypolicySerializer,
                    notificationSerializer)





class CreateOtherRowsInStaticTableView(generics.ListCreateAPIView):
    # permission_classes = [permissions.IsAuthenticated,]

    # permission_classes = [permissions.IsAuthenticated,]
    queryset = StaticSettingData.objects.all()
    serializer_class= CreateOtherRowsInStatictableSerializer


class UserIndustryDataView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated,]
    queryset = StaticSettingData.objects.filter(user_industry_data__isnull=False)
    serializer_class= UserIndustryDataSerializer

    def post(self, request):
        serializer = UserIndustryDataSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        errorcontext = {'user_industry_data': serializer.errors['user_industry_data'][0]}
        return Response(errorcontext, status=status.HTTP_400_BAD_REQUEST)



    def list(self, request):
        queryset = self.get_queryset()
        serializer = UserIndustryDataSerializer(queryset, many=True)
        context = {"data":serializer.data}
        return Response(context, status=status.HTTP_200_OK)


class UserAreaOfExperienceDataView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated,]    
    queryset = StaticSettingData.objects.filter(user_areaof_experience_data__isnull=False)
    serializer_class= UserAreaOfExperienceDataSerializer
    
    def post(self, request):
        serializer = UserAreaOfExperienceDataSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        errorcontext = {'user_areaof_experience_data': serializer.errors['user_areaof_experience_data'][0]}
        return Response(errorcontext, status=status.HTTP_400_BAD_REQUEST)


    def list(self, request):
        queryset = self.get_queryset()
        serializer = UserAreaOfExperienceDataSerializer(queryset, many=True)
        context = {"data":serializer.data}
        return Response(context, status=status.HTTP_200_OK)


class UserInterestedAreaDataView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated,]
    queryset = StaticSettingData.objects.filter(user_interested_area_data__isnull=False)
    serializer_class= UserInterestedAreaDataSerializer

    def post(self, request):
        serializer = UserInterestedAreaDataSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        errorcontext = {'user_interested_area_data': serializer.errors['user_interested_area_data'][0]}
        return Response(errorcontext, status=status.HTTP_400_BAD_REQUEST)


    def list(self, request):
        queryset = self.get_queryset()
        serializer = UserInterestedAreaDataSerializer(queryset, many=True)
        context = {"data":serializer.data}
        return Response(context, status=status.HTTP_200_OK)


class UserGoalDataView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated,]
    queryset = StaticSettingData.objects.filter(user_goal_data__isnull=False)
    serializer_class= UserGoalDataSerializer

    def post(self, request):
        serializer = UserGoalDataSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        errorcontext = {'user_goal_data': serializer.errors['user_goal_data'][0]}
        return Response(errorcontext, status=status.HTTP_400_BAD_REQUEST)


    def list(self, request):
        queryset = self.get_queryset()
        serializer = UserGoalDataSerializer(queryset, many=True)
        context = {"data":serializer.data}
        return Response(context, status=status.HTTP_200_OK)


class ConsultancyServiceCategoryDataView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated,]
    queryset = StaticSettingData.objects.filter(consultancyservice_category_data__isnull=False)
    serializer_class= ConsultancyServiceCategoryDataSerializer


    def post(self, request):
        serializer = ConsultancyServiceCategoryDataSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        errorcontext = {'consultancyservice_category_data': serializer.errors['consultancyservice_category_data'][0]}
        return Response(errorcontext, status=status.HTTP_400_BAD_REQUEST)


    def list(self, request):
        queryset = self.get_queryset()
        serializer = ConsultancyServiceCategoryDataSerializer(queryset, many=True)
        context = {"data":serializer.data}
        return Response(context, status=status.HTTP_200_OK)



class BlogTagDataView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated,]
    queryset = StaticSettingData.objects.filter(blog_tags_data__isnull=False)
    serializer_class= BlogTagDataSerializers

    def post(self, request):
        serializer = BlogTagDataSerializers(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        errorcontext = {'blog_tags_data': serializer.errors['blog_tags_data'][0]}
        return Response(errorcontext, status=status.HTTP_400_BAD_REQUEST)


    def list(self, request):
        queryset = self.get_queryset()
        serializer = BlogTagDataSerializers(queryset, many=True)
        # context = {"data":serializer.data}
        tags = []
        for data in serializer.data:
            data['blog_tags_data'] = data['blog_tags_data'].split(',')
            # print(data['blog_tags_data'])
            tags += data['blog_tags_data'] 
        # print(tags)
        context = {"data":tags}
        return Response(context, status=status.HTTP_200_OK)



class UserEducationDataView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated,]
    queryset = StaticSettingData.objects.filter(user_education_data__isnull=False)
    serializer_class= UserEducationDataSerializer

    def post(self, request):
        serializer = UserEducationDataSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        errorcontext = {'user_education_data': serializer.errors['user_education_data'][0]}
        return Response(errorcontext, status=status.HTTP_400_BAD_REQUEST)


    def list(self, request):
        queryset = self.get_queryset()
        serializer = UserEducationDataSerializer(queryset, many=True)
        context = {"data":serializer.data}
        return Response(context, status=status.HTTP_200_OK)



class FatchingTrubleView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated,]
    # queryset = StaticSettingData.objects.filter(fatching_truble__isnull=False)
    serializer_class= FacingtroubleSerializer

    def post(self, request):
        serializer = FacingtroubleSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        print(serializer.errors)
        # errorcontext = {'fatching_truble': serializer.errors['fatching_truble'][0]}
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    # def list(self, request):
    #     queryset = self.get_queryset()
    #     serializer = FacingtroubleSerializer(queryset, many=True)
    #     context = {"data":serializer.data}
    #     return Response(context, status=status.HTTP_200_OK)



class FaqView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated,]
    queryset = StaticSettingData.objects.filter(faq_title__isnull=False)
    serializer_class= FaqSerializer

    def list(self, request):
        queryset = self.get_queryset()
        serializer = FaqSerializer(queryset, many=True)
        context = {"data":serializer.data}
        return Response(context, status=status.HTTP_200_OK)



class privacypolicyView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated,]
    queryset = StaticSettingData.objects.filter(privacypolicy_title__isnull=False)
    serializer_class= privacypolicySerializer

    def list(self, request):
        queryset = self.get_queryset()
        serializer = privacypolicySerializer(queryset, many=True)
        context = {"data":serializer.data}
        return Response(context, status=status.HTTP_200_OK)



class NotificationView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated,]
    # queryset = Notification.objects.filter(user_id=request.user)
    # serializer_class= notificationSerializer
    

# send mail if 'user_mail_notification_enable'==true from 'User_settings'
    def post(self, request):
        # print("::::::::::::::::::",request.data)
        user = request.user
        if request.data['user'] == user.userid:
            serializer = notificationSerializer(data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            errorcontext = {'notification': serializer.errors}
            return Response(errorcontext, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("Bad Request",status=status.HTTP_400_BAD_REQUEST)
    
    def get_queryset(self):
            user = self.request.user
            # print("::::::::",user.userid)
            return Notification.objects.filter(user=user.userid)

    def list(self, request):
        user = request.user
        if request.data['user'] == user.userid:
            queryset = self.get_queryset()
            serializer = notificationSerializer(queryset, many=True)
            context = {"data":serializer.data}
            return Response(context, status=status.HTTP_200_OK)
        else:
            return Response("Bad Request",status=status.HTTP_400_BAD_REQUEST)
        
# need to remove 30 days previous notification from table

