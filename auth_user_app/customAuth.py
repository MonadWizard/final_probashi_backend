from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User

from .models import User


class CustomerBackendForPhoneNumber(ModelBackend):
    def authenticate(**kwargs):
        user_callphone = kwargs["user_callphone"]
        
        try:
            user_callphone = User.objects.get(user_callphone=user_callphone)
        except user_callphone.DoesNotExist:
            pass
        return user_callphone
