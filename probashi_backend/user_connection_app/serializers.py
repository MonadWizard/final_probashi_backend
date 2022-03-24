from rest_framework import serializers
from auth_user_app.models import User
from user_profile_app.models import User_education
from consultancy_app.models import ConsultancyCreate
from .models import UserFavoutireRequestSend, UserFavouriteList
from django.db.models import Q
from itertools import chain
from django.db.models import F



class UserEducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User_education
        fields = ['user_edu_degree']
class ConsultancySerializer(serializers.ModelSerializer):
    class Meta:
        model = ConsultancyCreate
        fields = ['consultant_service_category']
class SerachUserSerializer(serializers.ModelSerializer):
    user_educationdata = UserEducationSerializer(many=True, read_only=True)
    user_consultancydata = ConsultancySerializer(many=True, read_only=True)
    class Meta:
        model = User
        fields = ['userid', 'user_fullname', 'user_email', 'user_username', 'user_photopath', 'user_callphone',
                    'is_consultant', 'user_geolocation','user_areaof_experience', 
                    'user_industry','user_currentdesignation','user_educationdata', 'user_consultancydata']
        
        # exclude = ['is_staff','is_superuser','password','groups', 'user_permissions']


class UserFavouriteRequestSendSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFavoutireRequestSend
        fields = '__all__'


class UserFavouriteRequestsSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="userid.user_fullname")
    userphoto = serializers.ImageField(source="userid.user_photopath")
    is_consultant = serializers.BooleanField(source="userid.is_consultant")
    user_designation = serializers.CharField(source="userid.user_currentdesignation")
    user_location = serializers.ImageField(source="userid.user_geolocation")

    class Meta:
        model = UserFavoutireRequestSend
        fields = '__all__'


class AcceptFavouriteRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFavoutireRequestSend
        fields = ['is_favourite_accept']


class RejectFavouriteRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFavoutireRequestSend
        fields = ['is_favourite_reject']


class UserFavouriteListSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="userid.user_fullname")

    favourite_user = serializers.SerializerMethodField('get_favourite_user')

    def get_favourite_user(self, obj):
        
        user = self.context['user']
        print('user::::::::::::',user)
        # user_id = User.objects.filter(user_email=user).values('userid')
        # user_id = user_id[0].get('userid')
        # print('obj.user',obj.userid)
        if UserFavouriteList.objects.filter(userid=user):
            return obj.favourite_userid.userid
        elif UserFavouriteList.objects.filter(favourite_userid=user):
            return obj.userid.userid


        # favourite_data = UserFavouriteList.objects.filter(userid=user).values(favourite_user=F("favourite_userid"))
        # user_data = UserFavouriteList.objects.filter(favourite_userid=user).values(favourite_user=F('userid'))
        # data = list(chain(favourite_data, user_data))
        # return data

        
    class Meta:
        model = UserFavouriteList
        fields = ['username', 'favourite_user']




