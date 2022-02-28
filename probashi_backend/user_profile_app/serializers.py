from dataclasses import field, fields
from rest_framework import serializers
from auth_user_app.models import User

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_fullname_passport', 'user_username', 'user_gender', 'user_dob', 'user_photopath', 'user_residential_district', 'user_nonresidential_country', 'user_nonresidential_city', 'user_durationyear_abroad']


