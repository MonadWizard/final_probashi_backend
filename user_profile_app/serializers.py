from dataclasses import field
from pyexpat import model
from rest_framework import serializers
from auth_user_app.models import User
from .models import User_socialaccount_and_about, User_experience, User_education, User_idverification
from drf_extra_fields.fields import Base64ImageField
from consultancy_app.models import ConsultancyCreate


class UserProfileSkipPart0Serializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['is_user_serviceholder', 
                    'is_user_selfemployed', 'user_currentdesignation', 
                    'user_company_name', 'user_office_address'
                    ]
        extra_kwargs = {"__all__": {"error_messages": {"required": "field missing or incorrect"}}}
        



class UserProfileSkipPart1Serializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_current_location_durationyear', 
                    'user_industry', 'user_areaof_experience', 
                    'user_industry_experienceyear' 
                    ]
        extra_kwargs = {"__all__": {"error_messages": {"required": "field missing or incorrect"}}}

class UserProfileSkipPart2Serializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_interested_area', 'user_goal' ]
        extra_kwargs = {"__all__": {"error_messages": {"required": "field missing or incorrect"}}}


class UserEditPrifileSerializer(serializers.ModelSerializer):
    user_photopath=Base64ImageField() # From DRF Extra Fields
    class Meta:
        model = User
        fields = ['user_fullname_passport', 
                'user_username', 'user_gender',
                'user_dob','user_photopath']
        extra_kwargs = {"__all__": {"error_messages": {"required": "field missing or incorrect"}}}
    

class UserEditPrifileWithoutImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_fullname_passport', 
                'user_username', 'user_gender',
                'user_dob']
        extra_kwargs = {"__all__": {"error_messages": {"required": "field missing or incorrect"}}}
    


class UserInterestedAreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_interested_area']
        extra_kwargs = {"__all__": {"error_messages": {"required": "field missing or incorrect"}}}


class UserGoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_goal']
        extra_kwargs = {"__all__": {"error_messages": {"required": "field missing or incorrect"}}}


class UserSocialaccountAboutSerializer(serializers.ModelSerializer):
    class Meta:
        model = User_socialaccount_and_about
        fields = '__all__'
        extra_kwargs = {"__all__": {"error_messages": {"required": "field missing or incorrect"}}}

class UserSocialaccountAboutUpdatSerializer(serializers.ModelSerializer):
    class Meta:
        model = User_socialaccount_and_about
        fields = ['user_about', 'user_fbaccount', 'user_twitteraccount',
                    'user_instagramaccount', 'user_linkedinaccount',
                    'user_website', 'user_whatsapp_account', 'user_whatsapp_visibility',
                    'user_viber_account','user_immo_account']
        extra_kwargs = {"__all__": {"error_messages": {"required": "field missing or incorrect"}}}

class UserExperienceCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User_experience
        fields = '__all__'
        extra_kwargs = {"__all__": {"error_messages": {"required": "field missing or incorrect"}}}

class UserExperienceUpdatSerializer(serializers.ModelSerializer):
    class Meta:
        model = User_experience
        fields = ['id','user_designation', 'user_companyname', 'user_responsibilities',
                    'userexperience_startdate', 'userexperience_enddate']
        extra_kwargs = {"__all__": {"error_messages": {"required": "field missing or incorrect"}}}

        def update(self, instance, validated_data):
            validated_data.pop("id", None)
            return super().update(self, instance, validated_data)

class UserEducationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User_education
        fields = '__all__'
        extra_kwargs = {"__all__": {"error_messages": {"required": "field missing or incorrect"}}}

class UserIdVerificationCreateSerializer(serializers.ModelSerializer):
    user_verify_passportphoto_path=Base64ImageField()
    class Meta:
        model = User_idverification
        fields = '__all__'
        extra_kwargs = {"__all__": {"error_messages": {"required": "field missing or incorrect"}}}



class UserProfileViewSerializer(serializers.ModelSerializer):
    user_socialaboutdata = UserSocialaccountAboutSerializer(read_only=True)
    user_experiencedata = UserExperienceCreateSerializer(many=True, read_only=True)
    user_educationdata = UserEducationCreateSerializer(many=True, read_only=True)
    user_idverificationdata = UserIdVerificationCreateSerializer(many=True, read_only=True)
    class Meta:
        model = User
        # fields = ['userid' ,'user_fullname', 'user_photopath', 'is_consultant',
        #         'user_industry','user_geolocation','user_created_at',
        #         'user_interested_area','user_goal','user_industry_experienceyear',
        #         'user_areaof_experience','user_industry',
        #         'user_socialaboutdata','user_experiencedata', 'user_educationdata', 'user_idverificationdata']
        # fields = '__all__'
        # depth = 3
        exclude = ['is_staff','is_superuser','password','groups', 'user_permissions']
        extra_kwargs = {"__all__": {"error_messages": {"required": "field missing or incorrect"}}}



class UserConsultancyHomepageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConsultancyCreate
        fields = '__all__'
        extra_kwargs = {"__all__": {"error_messages": {"required": "field missing or incorrect"}}}


class UserProfileWithConsultancyViewSerializer(serializers.ModelSerializer):
    user_consultancydata = UserConsultancyHomepageSerializer(many=True, read_only=True)
    user_socialaboutdata = UserSocialaccountAboutSerializer(read_only=True)
    user_experiencedata = UserExperienceCreateSerializer(many=True, read_only=True)
    user_educationdata = UserEducationCreateSerializer(many=True, read_only=True)
    user_idverificationdata = UserIdVerificationCreateSerializer(many=True, read_only=True)
    class Meta:
        model = User
        # fields = ['userid' ,'user_fullname', 'user_photopath', 'is_consultant',
        #         'user_industry','user_geolocation','user_created_at',
        #         'user_interested_area','user_goal','user_industry_experienceyear',
        #         'user_areaof_experience','user_industry',
        #         'user_socialaboutdata','user_experiencedata', 'user_educationdata', 'user_idverificationdata']
        # fields = '__all__'
        # depth = 3
        exclude = ['is_staff','is_superuser','password','groups', 'user_permissions']
        extra_kwargs = {"__all__": {"error_messages": {"required": "field missing or incorrect"}}}







