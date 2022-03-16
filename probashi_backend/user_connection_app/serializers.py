from xml.etree.ElementInclude import include
from rest_framework import serializers
from auth_user_app.models import User
from user_profile_app.models import User_education
from consultancy_app.models import ConsultancyCreate
from .models import UserFavoutireRequestSend

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
                    'user_industry','user_educationdata', 'user_consultancydata']
        
        # include = ['user_educationdata']
        # exclude = ['is_staff','is_superuser','password','groups', 'user_permissions']


class UserFavouriteRequestSendSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFavoutireRequestSend
        fields = '__all__'


class UserFavouriteRequestsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFavoutireRequestSend
        fields = '__all__'

