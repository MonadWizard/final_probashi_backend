from dataclasses import field, fields
from rest_framework import serializers
from auth_user_app.models import User
from .models import User_socialaccount_and_about, User_experience, User_education, User_idverification

class UserProfileSkipPart1Serializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_current_location_durationyear', 
                    'user_industry', 'user_areaof_experience', 
                    'user_industry_experienceyear' 
                    ]

class UserProfileSkipPart2Serializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_interested_area', 'user_goal' ]


class UserSocialaccountAboutSerializer(serializers.ModelSerializer):
    class Meta:
        model = User_socialaccount_and_about
        fields = '__all__'

