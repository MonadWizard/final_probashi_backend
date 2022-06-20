from django.contrib import admin
from .models import User, PhoneOTP, mailVerify, user_unmatch

from rest_framework_simplejwt.token_blacklist import models
from rest_framework_simplejwt.token_blacklist.admin import OutstandingTokenAdmin


class UserAdmin(admin.ModelAdmin):
    list_display = ["user_fullname", "user_email", "user_callphone", "user_created_at"]


admin.site.register(User, UserAdmin)
# admin.site.register(User)


# FOR REMOVE USER WITH THEIR OUTSTANDING TOKENS
class NewOutstandingTokenAdmin(OutstandingTokenAdmin):
    def has_delete_permission(self, *args, **kwargs):
        return True


admin.site.unregister(models.OutstandingToken)
admin.site.register(models.OutstandingToken, NewOutstandingTokenAdmin)

admin.site.register(PhoneOTP)
admin.site.register(mailVerify)

class user_unmatchAdmin(admin.ModelAdmin):
    list_display = ["user_id", "user_unmatch", "user_unmatch_created_at"]

admin.site.register(user_unmatch, user_unmatchAdmin)
# admin.site.register(user_unmatch)