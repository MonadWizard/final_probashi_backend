from email.policy import default
from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import AbstractBaseUser, \
                                        BaseUserManager, \
                                        PermissionsMixin

from rest_framework_simplejwt.tokens import RefreshToken

from datetime import datetime, timedelta



class UserManager(BaseUserManager):

    def create_user(self,userid, user_fullname, user_email, password=None):
        if userid is None:
            raise TypeError('User ID should not be none')
        if user_fullname is None:
            raise TypeError('Users should have a fullname')
        if user_email is None:
            raise TypeError('Users should have a Email')

        user = self.model(userid=userid, user_fullname=user_fullname, user_email=self.normalize_email(user_email))
        user.set_password(password)
        user.save()
        return user

    def create_user_phone(self,userid, user_fullname,  user_callphone, password=None):
        if userid is None:
            raise TypeError('User ID should not be none')
        if user_fullname is None:
            raise TypeError('Users should have a fullname')
        if user_callphone is None:
            raise TypeError('Users should have a Call Phone Number')

        user = self.model(userid=userid, user_fullname=user_fullname,user_callphone=user_callphone)
        # user.set_password(password)
        user.save()
        return user





    def create_superuser(self,userid, user_fullname, user_email, password=None):
        if userid is None:
            raise TypeError('User ID should not be none')
        if password is None:
            raise TypeError('Password should not be none')

        user = self.create_user(userid, user_fullname, user_email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user


AUTH_PROVIDERS = {'facebook': 'facebook','google': 'google',
                    'linkedin': 'linkedin', 'email': 'email'}


class User(AbstractBaseUser, PermissionsMixin):
    userid= models.CharField(primary_key=True, max_length=30, unique=True, db_index=True)
    user_fullname = models.CharField(max_length=255, db_index=True)
    user_email = models.EmailField(max_length=255, unique=True, db_index=True, blank=True, null=True)
    is_verified = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_consultant = models.BooleanField(default=False)
    user_created_at = models.DateTimeField(auto_now_add=True)
    # user_updated_at = models.DateTimeField(auto_now=True)
    # user_promocode_pk = 
    user_callphone = models.CharField(max_length=30, unique=True, db_index=True, blank=True, null=True)
    user_geolocation = models.CharField(max_length=200, db_index=True, blank=True, null=True)
    user_device_typeserial= models.CharField(max_length=30, blank=True, null=True, db_index=True)
    user_fullname_passport= models.CharField(max_length=200, blank=True, null=True)
    user_username = models.CharField(max_length=100, unique=True, blank=True, null=True)
    user_gender = models.CharField(max_length=20, blank=True, null=True)
    user_dob = models.DateField(blank=True, null=True)
    user_photopath = models.ImageField(upload_to='user/profile_picture', blank=True, null=True)
    user_residential_district = models.CharField(max_length=200, blank=True, null=True)
    user_nonresidential_country = models.CharField(max_length=200, blank=True, null=True)
    user_nonresidential_city = models.CharField(max_length=200, blank=True, null=True)
    user_durationyear_abroad = models.IntegerField(default=0)
    
    user_current_location_durationyear = models.IntegerField(blank=True, null=True)
    user_industry = models.CharField(max_length=200, blank=True, null=True)
    user_areaof_experience = models.CharField(max_length=200, blank=True, null=True)
    user_industry_experienceyear = models.IntegerField(blank=True, null=True)
    
    user_interested_area = ArrayField(models.CharField(max_length=200), blank=True, null=True)
    user_goal = ArrayField(models.CharField(max_length=200), blank=True, null=True)
    
    is_user_serviceholder = models.BooleanField(default=False)
    is_user_selfemployed = models.BooleanField(default=False)
    user_currentdesignation = models.CharField(max_length=200, blank=True, null=True)
    user_company_name = models.CharField(max_length=200, blank=True, null=True)
    user_office_address = models.CharField(max_length=200, blank=True, null=True)

    auth_provider = models.CharField(max_length=255, blank=False,
                                    null=False, default=AUTH_PROVIDERS.get('email'))

    USERNAME_FIELD = 'user_email'
    REQUIRED_FIELDS = ['userid','user_fullname']

    objects = UserManager()

    def __str__(self):
        return self.user_fullname

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }



class PhoneOTP(models.Model):
    user_callphone = models.CharField(max_length=30, unique=True, db_index=True)
    otp = models.CharField(max_length=4, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(default=datetime.now()+timedelta(minutes=5))
    is_used = models.BooleanField(default=False)

    def __str__(self):
        return self.otp

