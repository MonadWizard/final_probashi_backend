from django.db import models

# Create your models here.
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin)

from django.db import models
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
    user_created_at = models.DateTimeField(auto_now_add=True)
    user_updated_at = models.DateTimeField(auto_now=True)


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






