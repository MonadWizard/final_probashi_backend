from dataclasses import field, fields
from rest_framework import serializers
from auth_user_app.models import User

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
