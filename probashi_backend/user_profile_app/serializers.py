from dataclasses import field
from pyexpat import model
from rest_framework import serializers
from auth_user_app.models import User
from .models import User_socialaccount_and_about, User_experience, User_education, User_idverification
from drf_extra_fields.fields import Base64ImageField

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


class UserEditPrifileSerializer(serializers.ModelSerializer):
    user_photopath=Base64ImageField() # From DRF Extra Fields
    class Meta:
        model = User
        fields = ['user_fullname_passport', 
                'user_username', 'user_gender',
                'user_dob','user_photopath']
    
    # def create(self, validated_data):
    #     user_photopath=validated_data.pop('user_photopath')
    #     return User.objects.create(user_photopath=user_photopath)



class UserSocialaccountAboutCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User_socialaccount_and_about
        fields = '__all__'

class UserSocialaccountAboutUpdatSerializer(serializers.ModelSerializer):
    class Meta:
        model = User_socialaccount_and_about
        fields = ['user_about', 'user_fbaccount', 'user_twitteraccount',
                    'user_instagramaccount', 'user_linkedinaccount',
                    'user_website', 'user_whatsapp_account', 'user_whatsapp_visibility',
                    'user_viber_account','user_immo_account']

class UserExperienceCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User_experience
        fields = '__all__'

class UserExperienceUpdatSerializer(serializers.ModelSerializer):
    class Meta:
        model = User_experience
        fields = ['id','user_designation', 'user_companyname', 'user_responsibilities',
                    'userexperience_startdate', 'userexperience_enddate']
        # lookup_field = 'id'

        def update(self, instance, validated_data):
            validated_data.pop("id", None)
            return super().update(self, instance, validated_data)

class UserEducationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User_education
        fields = '__all__'

class UserIdVerificationCreateSerializer(serializers.ModelSerializer):
    user_verify_passportphoto_path=Base64ImageField()
    class Meta:
        model = User_idverification
        fields = '__all__'










class UserSocialLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = User_socialaccount_and_about
        fields = '__all__'

class UserExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = User_experience
        fields = '__all__'

class UserEducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User_education
        fields = '__all__'

class UserIDverificationSerializer(serializers.ModelSerializer):
    # user_socialaboutdata = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = User_idverification
        # fields = ['userid', 'is_user_permanent_resident', 'user_verify_id_type', 'user_verify_passportphoto_path']   
        fields = '__all__'
class UserProfileViewSerializer(serializers.ModelSerializer):
    user_socialaboutdata = UserSocialLinkSerializer(read_only=True)
    user_experiencedata = UserExperienceSerializer(many=True, read_only=True)
    user_educationdata = UserEducationSerializer(many=True, read_only=True)
    user_idverificationdata = UserIDverificationSerializer(many=True, read_only=True)
    class Meta:
        model = User
        fields = ['userid' ,'user_fullname', 'user_photopath', 'is_consultant',
                'user_industry','user_geolocation','user_created_at',
                'user_interested_area','user_goal','user_industry_experienceyear',
                'user_areaof_experience','user_industry',
                'user_socialaboutdata','user_experiencedata', 'user_educationdata', 'user_idverificationdata']
        # fields = '__all__'
        depth = 2







