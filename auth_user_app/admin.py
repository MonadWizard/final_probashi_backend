from import_export.admin import ImportExportModelAdmin
from django.contrib import admin
from .models import User, PhoneOTP, mailVerify, user_unmatch


from .resource import (
    UserDataPropertyAdminResource,
    PhoneOTPPropertyAdminResource,
    mailVerifyPropertyAdminResource,
    user_unmatchPropertyAdminResource
)

from rest_framework_simplejwt.token_blacklist import models
from rest_framework_simplejwt.token_blacklist.admin import OutstandingTokenAdmin


# class UserAdmin(admin.ModelAdmin):
#     list_display = ["user_fullname", "user_email", "user_callphone", "user_created_at"]


@admin.register(User)
class UserAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = UserDataPropertyAdminResource
    list_display = ["user_fullname", "user_email", "user_callphone", "user_created_at"]


@admin.register(PhoneOTP)
class PhoneOTPAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = PhoneOTPPropertyAdminResource
    # list_display = ["user_fullname", "user_email", "user_callphone", "user_created_at"]


@admin.register(mailVerify)
class mailVerifyAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = mailVerifyPropertyAdminResource
    # list_display = ["user_fullname", "user_email", "user_callphone", "user_created_at"]


@admin.register(user_unmatch)
class user_unmatchAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = user_unmatchPropertyAdminResource
    list_display = ["user_id", "user_unmatch", "user_unmatch_created_at"]



# admin.site.register(User, UserAdmin)
# admin.site.register(User)


# FOR REMOVE USER WITH THEIR OUTSTANDING TOKENS
class NewOutstandingTokenAdmin(OutstandingTokenAdmin):
    def has_delete_permission(self, *args, **kwargs):
        return True


admin.site.unregister(models.OutstandingToken)
admin.site.register(models.OutstandingToken, NewOutstandingTokenAdmin)

# admin.site.register(PhoneOTP)
# admin.site.register(mailVerify)

# class user_unmatchAdmin(admin.ModelAdmin):
#     list_display = ["user_id", "user_unmatch", "user_unmatch_created_at"]

# admin.site.register(user_unmatch, user_unmatchAdmin)
# admin.site.register(user_unmatch)