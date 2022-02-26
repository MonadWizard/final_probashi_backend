from django.db import models

# Create your models here.
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin)

from django.db import models
from rest_framework_simplejwt.tokens import RefreshToken


class UserManager(BaseUserManager):

    def create_user(self,userid, fullname, email, password=None):
        if userid is None:
            raise TypeError('User ID should not be none')
        if fullname is None:
            raise TypeError('Users should have a fullname')
        if email is None:
            raise TypeError('Users should have a Email')

        user = self.model(userid=userid, fullname=fullname, email=self.normalize_email(email))
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self,userid, fullname, email, password=None):
        if userid is None:
            raise TypeError('User ID should not be none')
        if password is None:
            raise TypeError('Password should not be none')

        user = self.create_user(userid, fullname, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user


AUTH_PROVIDERS = {'facebook': 'facebook', 'google': 'google',
                    'twitter': 'twitter', 'email': 'email'}


class User(AbstractBaseUser, PermissionsMixin):
    userid= models.CharField(primary_key=True,max_length=30, unique=True, db_index=True)
    fullname = models.CharField(max_length=255, unique=True, db_index=True)
    email = models.EmailField(max_length=255, unique=True, db_index=True)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    auth_provider = models.CharField(
        max_length=255, blank=False,
        null=False, default=AUTH_PROVIDERS.get('email'))

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['userid','fullname']

    objects = UserManager()

    def __str__(self):
        return self.email

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }
