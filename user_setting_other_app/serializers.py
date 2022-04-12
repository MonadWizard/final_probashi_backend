from rest_framework import serializers
from .models import StaticSettingData, Facing_trouble, Notification, User_settings
from drf_extra_fields.fields import Base64ImageField


class UserIndustryDataSerializer(serializers.ModelSerializer):
    class Meta:
        model=StaticSettingData
        fields=['user_industry_data']
        extra_kwargs = {"__all__": {"error_messages": {"required": "field missing or incorrect"}}}


class UserAreaOfExperienceDataSerializer(serializers.ModelSerializer):

    class Meta:
        model=StaticSettingData
        fields=['user_areaof_experience_data']
        extra_kwargs = {"__all__": {"error_messages": {"required": "field missing or incorrect"}}}



class UserInterestedAreaDataSerializer(serializers.ModelSerializer):
    class Meta:
        model=StaticSettingData
        fields=['user_interested_area_data']
        extra_kwargs = {"__all__": {"error_messages": {"required": "field missing or incorrect"}}}


class UserGoalDataSerializer(serializers.ModelSerializer):
    

    class Meta:
        model=StaticSettingData
        fields=['user_goal_data']
        error_messages = {"user_goal_data": "static_setting_data with this user goal data already exists."}
        extra_kwargs = {"__all__": {"error_messages": {"required": "field missing or incorrect"}}}


class ConsultancyServiceCategoryDataSerializer(serializers.ModelSerializer):
    class Meta:
        model=StaticSettingData
        fields=['consultancyservice_category_data']
        extra_kwargs = {"__all__": {"error_messages": {"required": "field missing or incorrect"}}}
    
    

class CreateOtherRowsInStatictableSerializer(serializers.ModelSerializer):
    class Meta:
        model=StaticSettingData
        fields=['user_industry_data',
                'user_areaof_experience_data',
                'user_interested_area_data',
                'user_goal_data',
                'consultancyservice_category_data']
        extra_kwargs = {"__all__": {"error_messages": {"required": "field missing or incorrect"}}}



class BlogTagDataSerializers(serializers.ModelSerializer):
    class Meta:
        model=StaticSettingData
        fields=['blog_tags_data']
        extra_kwargs = {"__all__": {"error_messages": {"required": "field missing or incorrect"}}}



class UserEducationDataSerializer(serializers.ModelSerializer):
    class Meta:
        model=StaticSettingData
        fields=['user_education_data']
        extra_kwargs = {"__all__": {"error_messages": {"required": "field missing or incorrect"}}}



class FacingtroubleSerializer(serializers.ModelSerializer):
    user_problem_photo_path=Base64ImageField() # From DRF Extra Fields
    class Meta:
        model = Facing_trouble
        fields = '__all__'
        extra_kwargs = {"__all__": {"error_messages": {"required": "field missing or incorrect"}}}



class FaqSerializer(serializers.ModelSerializer):
    class Meta:
        model=StaticSettingData
        fields=['faq_title', 'faq_description']
        extra_kwargs = {"__all__": {"error_messages": {"required": "field missing or incorrect"}}}


class privacypolicySerializer(serializers.ModelSerializer):
    class Meta:
        model=StaticSettingData
        fields=['privacypolicy_title', 'privacypolicy_descriptions']
        extra_kwargs = {"__all__": {"error_messages": {"required": "field missing or incorrect"}}}


class notificationSerializer(serializers.ModelSerializer):
    class Meta:
        model=Notification
        fields='__all__'
        extra_kwargs = {"__all__": {"error_messages": {"required": "field missing or incorrect"}}}


class updateNotificationStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model=Notification
        fields=['is_notification_seen']
        extra_kwargs = {"__all__": {"error_messages": {"required": "field missing or incorrect"}}}


class DeleteNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model=Notification
        fields=['is_notification_delete']
        extra_kwargs = {"__all__": {"error_messages": {"required": "field missing or incorrect"}}}



class UserSettingsOptionViewSerializer(serializers.ModelSerializer):
    class Meta:
        model=User_settings
        fields=['user_mail_notification_enable', 'user_monthly_newsleter_enable']
        extra_kwargs = {"__all__": {"error_messages": {"required": "field missing or incorrect"}}}


# -----------------------------x--------------------------x--------------------------------x---------------------

class EducationServiceDataSerializer(serializers.ModelSerializer):
    class Meta:
        model=StaticSettingData
        fields=['educationService_degree']
        extra_kwargs = {"__all__": {"error_messages": {"required": "field missing or incorrect"}}}

class OverseasRecruitmentServiceDataSerializer(serializers.ModelSerializer):
    class Meta:
        model=StaticSettingData
        fields=['overseasrecruitmentservice_job_type']
        extra_kwargs = {"__all__": {"error_messages": {"required": "field missing or incorrect"}}}


class MedicalConsultancyServiceDataSerializer(serializers.ModelSerializer):
    class Meta:
        model=StaticSettingData
        fields=['medicalconsultancyservice_treatment_area']
        extra_kwargs = {"__all__": {"error_messages": {"required": "field missing or incorrect"}}}

class LegalCivilServiceDataSerializer(serializers.ModelSerializer):
    class Meta:
        model=StaticSettingData
        fields=['legalcivilservice_required', 'legalcivilservice_issue']
        extra_kwargs = {"__all__": {"error_messages": {"required": "field missing or incorrect"}}}


class PropertyManagementServiceDataSerializer(serializers.ModelSerializer):
    class Meta:
        model=StaticSettingData
        fields=['propertymanagementservice_propertylocation',
                'propertymanagementservice_type', 
                'propertymanagementservice_need']
        extra_kwargs = {"__all__": {"error_messages": {"required": "field missing or incorrect"}}}


class TourismServiceDataSerializer(serializers.ModelSerializer):
    class Meta:
        model=StaticSettingData
        fields=['tourismservices']
        extra_kwargs = {"__all__": {"error_messages": {"required": "field missing or incorrect"}}}


class TrainingServiceDataSerializer(serializers.ModelSerializer):
    class Meta:
        model=StaticSettingData
        fields=['trainingservice_topic', 'trainingservice_duration']
        extra_kwargs = {"__all__": {"error_messages": {"required": "field missing or incorrect"}}}


class DigitalServiceDataSerializer(serializers.ModelSerializer):
    class Meta:
        model=StaticSettingData
        fields=['digitalservice_type']
        extra_kwargs = {"__all__": {"error_messages": {"required": "field missing or incorrect"}}}


class TradeFacilitationServiceDataSerializer(serializers.ModelSerializer):
    class Meta:
        model=StaticSettingData
        fields=['tradefacilitationservice_type', 'tradefacilitationservice_Purpose']
        extra_kwargs = {"__all__": {"error_messages": {"required": "field missing or incorrect"}}}









