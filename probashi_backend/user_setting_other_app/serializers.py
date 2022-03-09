from rest_framework import serializers
from .models import StaticSettingData

class UserIndustryDataSerializer(serializers.ModelSerializer):
    class Meta:
        model=StaticSettingData
        fields=['user_industry_data']


class UserAreaOfExperienceDataSerializer(serializers.ModelSerializer):

    class Meta:
        model=StaticSettingData
        fields=['user_areaof_experience_data']



class UserInterestedAreaDataSerializer(serializers.ModelSerializer):
    class Meta:
        model=StaticSettingData
        fields=['user_interested_area_data']


class UserGoalDataSerializer(serializers.ModelSerializer):
    class Meta:
        model=StaticSettingData
        fields=['user_goal_data']

class ConsultancyServiceCategoryDataSerializer(serializers.ModelSerializer):
    class Meta:
        model=StaticSettingData
        fields=['consultancyservice_category_data']





