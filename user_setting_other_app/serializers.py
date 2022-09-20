from rest_framework import serializers
from .models import StaticSettingData, Facing_trouble, Notification, User_settings
from drf_extra_fields.fields import Base64ImageField


class UserIndustryDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaticSettingData
        fields = ["user_industry_data"]


class UserAreaOfExperienceDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaticSettingData
        fields = ["user_areaof_experience_data"]

class UserCurrentDesignationDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaticSettingData
        fields = ["user_current_designation"]



class UserInterestedAreaDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaticSettingData
        fields = ["user_interested_area_data"]


class UserGoalDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaticSettingData
        fields = ["user_goal_data"]
        error_messages = {
            "user_goal_data": "static_setting_data with this user goal data already exists."
        }


class ConsultancyServiceCategoryDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaticSettingData
        fields = ["consultancyservice_category_data"]


class CreateOtherRowsInStatictableSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaticSettingData
        fields = [
            "user_industry_data",
            "user_areaof_experience_data",
            "user_interested_area_data",
            "user_goal_data",
            "consultancyservice_category_data",
        ]


class BlogTagDataSerializers(serializers.ModelSerializer):
    class Meta:
        model = StaticSettingData
        fields = ["blog_tags_data"]


class UserEducationDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaticSettingData
        fields = ["user_education_data"]


class FacingtroubleSerializer(serializers.ModelSerializer):
    user_problem_photo_path = Base64ImageField()  # From DRF Extra Fields

    class Meta:
        model = Facing_trouble
        fields = "__all__"


class FaqSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaticSettingData
        fields = ["faq_title", "faq_description"]


class privacypolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = StaticSettingData
        fields = ["privacypolicy_title", "privacypolicy_descriptions"]


class notificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = "__all__"


class updateNotificationStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ["is_notification_seen"]


class DeleteNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ["is_notification_delete"]


class UserSettingsOptionViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = User_settings
        fields = ["user_mail_notification_enable", "user_monthly_newsleter_enable"]


class EducationServiceDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaticSettingData
        fields = ["educationService_degree"]


class OverseasRecruitmentServiceDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaticSettingData
        fields = ["overseasrecruitmentservice_job_type"]


class MedicalConsultancyServiceDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaticSettingData
        fields = ["medicalconsultancyservice_treatment_area"]


class LegalCivilServiceDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaticSettingData
        fields = ["legalcivilservice_required", "legalcivilservice_issue"]


class PropertyManagementServiceDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaticSettingData
        fields = [
            "propertymanagementservice_propertylocation",
            "propertymanagementservice_type",
            "propertymanagementservice_need",
        ]


class TourismServiceDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaticSettingData
        fields = ["tourismservices"]


class TrainingServiceDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaticSettingData
        fields = ["trainingservice_topic", "trainingservice_duration"]


class DigitalServiceDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaticSettingData
        fields = ["digitalservice_type"]


class TradeFacilitationServiceDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaticSettingData
        fields = ["tradefacilitationservice_type", "tradefacilitationservice_Purpose"]


class GetCitySerializer(serializers.ModelSerializer):
    class Meta:
        model = StaticSettingData
        fields = ["state_name"]
