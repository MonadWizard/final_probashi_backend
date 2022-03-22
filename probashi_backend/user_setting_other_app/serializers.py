from rest_framework import serializers
from .models import StaticSettingData, Facing_trouble
from drf_extra_fields.fields import Base64ImageField


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
        error_messages = {"user_goal_data": "static_setting_data with this user goal data already exists."}


class ConsultancyServiceCategoryDataSerializer(serializers.ModelSerializer):
    class Meta:
        model=StaticSettingData
        fields=['consultancyservice_category_data']
    
    

class CreateOtherRowsInStatictableSerializer(serializers.ModelSerializer):
    class Meta:
        model=StaticSettingData
        fields=['user_industry_data',
                'user_areaof_experience_data',
                'user_interested_area_data',
                'user_goal_data',
                'consultancyservice_category_data']



class BlogTagDataSerializers(serializers.ModelSerializer):
    class Meta:
        model=StaticSettingData
        fields=['blog_tags_data']



class UserEducationDataSerializer(serializers.ModelSerializer):
    class Meta:
        model=StaticSettingData
        fields=['user_education_data']



class FacingtroubleSerializer(serializers.ModelSerializer):
    user_problem_photo_path=Base64ImageField() # From DRF Extra Fields
    class Meta:
        model = Facing_trouble
        fields = '__all__'


