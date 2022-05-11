from django.contrib import admin
from .models import User, PhoneOTP, mailVerify 

from rest_framework_simplejwt.token_blacklist import models
from rest_framework_simplejwt.token_blacklist.admin import OutstandingTokenAdmin



class UserAdmin(admin.ModelAdmin):
    list_display = ['user_fullname', 'user_email', 'user_created_at']
admin.site.register(User, UserAdmin)

# FOR REMOVE USER WITH THEIR OUTSTANDING TOKENS
class NewOutstandingTokenAdmin(OutstandingTokenAdmin):
    
    def has_delete_permission(self, *args, **kwargs):
        return True
admin.site.unregister(models.OutstandingToken)
admin.site.register(models.OutstandingToken, NewOutstandingTokenAdmin)

admin.site.register(PhoneOTP)
admin.site.register(mailVerify)