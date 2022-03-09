from xml.etree.ElementInclude import include
from rest_framework import serializers
from auth_user_app.models import User
from user_profile_app.models import User_education

class UserEducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User_education
        fields = ['user_edu_degree']

class SerachUserSerializer(serializers.ModelSerializer):
    user_educationdata = UserEducationSerializer(many=True, read_only=True)

    class Meta:
        model = User
        # fields = ['user_fullname', 'user_areaof_experience', 'user_geolocation', 'user_educationdata']
        
        include = ['user_educationdata']
        exclude = ['is_staff','is_superuser','password','groups', 'user_permissions']









