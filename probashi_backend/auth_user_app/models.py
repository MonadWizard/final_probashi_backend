from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import AbstractBaseUser, \
                                        BaseUserManager, \
                                        PermissionsMixin

from rest_framework_simplejwt.tokens import RefreshToken

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


class User(AbstractBaseUser, PermissionsMixin):
    userid= models.CharField(primary_key=True,max_length=30, unique=True, db_index=True)
    user_fullname = models.CharField(max_length=255, unique=True, db_index=True)
    user_email = models.EmailField(max_length=255, unique=True, db_index=True)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_consultant = models.BooleanField(default=False)
    user_created_at = models.DateTimeField(auto_now_add=True)
    # user_updated_at = models.DateTimeField(auto_now=True)
    # user_promocode_pk = 
    user_callphone = models.CharField(max_length=30, unique=True, db_index=True, blank=True, null=True)
    user_geolocation = models.CharField(max_length=200, db_index=True, blank=True, null=True)
    user_device_typeserial= models.CharField(max_length=30, unique=True, blank=True, null=True, db_index=True)
    user_fullname_passport= models.CharField(max_length=200, blank=True, null=True)
    user_username = models.CharField(max_length=100, unique=True, blank=True, null=True)
    user_gender = models.CharField(max_length=20, blank=True, null=True)
    user_dob = models.DateField(blank=True, null=True)
    user_photopath = models.CharField(max_length=200, blank=True, null=True)
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
    # user_consuttype_personal = models.BooleanField(default=False)
    # user_consulttype_company = models.BooleanField(default=False)

    # no need
    # user_social_and_about_pk = models.ForeignKey(user_socialaccount_and_about, on_delete=models.DO_NOTHING)
    # user_experience_pk =
    # user_education_pk = 
    # user_IDverification_pk =
    # user_consultant_pk =  


    USERNAME_FIELD = 'user_email'
    REQUIRED_FIELDS = ['userid','user_fullname']

    objects = UserManager()

    def __str__(self):
        return self.user_email

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }






