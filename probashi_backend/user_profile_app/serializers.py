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
    
    def create(self, validated_data):
        user_photopath=validated_data.pop('user_photopath')
        return User.objects.create(user_photopath=user_photopath)



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
        fields = ['user_designation', 'user_companyname', 'user_responsibilities',
                    'userexperience_startdate', 'userexperience_enddate']






