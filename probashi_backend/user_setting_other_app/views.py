from rest_framework import generics, status, views, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import permissions
from django.http import Http404
from .models import StaticSettingData
from .serializers import (UserIndustryDataSerializer,
                    UserAreaOfExperienceDataSerializer,
                    UserInterestedAreaDataSerializer,
                    UserGoalDataSerializer,
                    ConsultancyServiceCategoryDataSerializer)


class UserIndustryDataView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated,]
    queryset = StaticSettingData.objects.filter(user_industry_data__isnull=False)
    serializer_class= UserIndustryDataSerializer


class UserAreaOfExperienceDataView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated,]    
    queryset = StaticSettingData.objects.filter(user_areaof_experience_data__isnull=False)
    serializer_class= UserAreaOfExperienceDataSerializer


class UserInterestedAreaDataView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated,]
    queryset = StaticSettingData.objects.filter(user_interested_area_data__isnull=False)
    serializer_class= UserInterestedAreaDataSerializer


class UserGoalDataView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated,]
    queryset = StaticSettingData.objects.filter(user_goal_data__isnull=False)
    serializer_class= UserGoalDataSerializer


class ConsultancyServiceCategoryDataView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated,]
    queryset = StaticSettingData.objects.filter(consultancyservice_category_data__isnull=False)
    serializer_class= ConsultancyServiceCategoryDataSerializer







