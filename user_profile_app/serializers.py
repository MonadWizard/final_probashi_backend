from rest_framework import serializers
from auth_user_app.models import User
from .models import (
    User_socialaccount_and_about,
    User_experience,
    User_education,
    User_idverification,
)
from drf_extra_fields.fields import Base64ImageField
from consultancy_app.models import ConsultancyCreate


class UserProfileSkipPart0Serializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "is_user_serviceholder",
            "is_user_selfemployed",
            "user_currentdesignation",
            "user_company_name",
            "user_office_address",
        ]


class UserProfileSkipPart1Serializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "user_current_location_durationyear",
            "user_industry",
            "user_areaof_experience",
            "user_industry_experienceyear",
        ]


class UserProfileSkipPart2Serializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["user_interested_area", "user_goal"]


class UserEditPrifileSerializer(serializers.ModelSerializer):
    user_photopath = Base64ImageField()  # From DRF Extra Fields

    class Meta:
        model = User
        fields = [
            "user_fullname_passport",
            "user_username",
            "user_gender",
            "user_dob",
            "user_photopath",
        ]


class UserEditPrifileWithoutImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["user_fullname_passport", "user_username", "user_gender", "user_dob"]


class UserInterestedAreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["user_interested_area"]


class UserGoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["user_goal"]


class UserSocialaccountAboutSerializer(serializers.ModelSerializer):
    class Meta:
        model = User_socialaccount_and_about
        fields = "__all__"


class UserSocialaccountAboutUpdatSerializer(serializers.ModelSerializer):
    class Meta:
        model = User_socialaccount_and_about
        fields = [
            "user_about",
            "user_fbaccount",
            "user_twitteraccount",
            "user_instagramaccount",
            "user_linkedinaccount",
            "user_website",
            "user_whatsapp_account",
            "user_whatsapp_visibility",
            "user_viber_account",
            "user_immo_account",
        ]


class UserExperienceCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User_experience
        fields = "__all__"


class UserExperienceUpdatSerializer(serializers.ModelSerializer):
    class Meta:
        model = User_experience
        fields = [
            "id",
            "user_designation",
            "user_companyname",
            "user_responsibilities",
            "userexperience_startdate",
            "userexperience_enddate",
        ]

        def update(self, instance, validated_data):
            validated_data.pop("id", None)
            return super().update(self, instance, validated_data)


class UserEducationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User_education
        fields = "__all__"


class UserIdVerificationCreateSerializer(serializers.ModelSerializer):
    user_verify_passportphoto_path = Base64ImageField()

    class Meta:
        model = User_idverification
        fields = "__all__"


class UserProfileViewSerializer(serializers.ModelSerializer):
    user_socialaboutdata = UserSocialaccountAboutSerializer(read_only=True)
    user_experiencedata = UserExperienceCreateSerializer(many=True, read_only=True)
    user_educationdata = UserEducationCreateSerializer(many=True, read_only=True)
    user_idverificationdata = UserIdVerificationCreateSerializer(
        many=True, read_only=True
    )

    class Meta:
        model = User
        
        exclude = ["is_staff", "is_superuser", "password", "groups", "user_permissions"]


class UserConsultancyHomepageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConsultancyCreate
        fields = "__all__"


class UserProfileWithConsultancyViewSerializer(serializers.ModelSerializer):
    user_consultancydata = UserConsultancyHomepageSerializer(many=True, read_only=True)
    user_socialaboutdata = UserSocialaccountAboutSerializer(read_only=True)
    user_experiencedata = UserExperienceCreateSerializer(many=True, read_only=True)
    user_educationdata = UserEducationCreateSerializer(many=True, read_only=True)
    user_idverificationdata = UserIdVerificationCreateSerializer(
        many=True, read_only=True
    )

    class Meta:
        model = User
        exclude = ["is_staff", "is_superuser", "password", "groups", "user_permissions"]
