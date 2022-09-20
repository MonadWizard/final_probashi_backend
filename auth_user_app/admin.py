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



@admin.register(User)
class UserAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = UserDataPropertyAdminResource
    list_display = ["user_fullname", "user_email", "user_callphone", "user_created_at",
    "is_active", "is_consultant", "is_superuser", "is_staff", "is_pro_user", "pro_user_created_at", "user_geolocation",
    "user_device_typeserial", "user_username", "user_gender", "user_dob", "user_photopath",
    "user_residential_district", "user_nonresidential_country", "user_nonresidential_city", "user_durationyear_abroad",
    "user_current_location_durationyear", "user_industry", "user_areaof_experience", "user_industry_experienceyear",
    "user_interested_area", "user_goal", "is_user_serviceholder", "is_user_selfemployed", "user_currentdesignation",
    "user_company_name", "user_office_address", "auth_provider"]
    list_per_page = 20 
    list_display_links = ["user_fullname", "user_email", "user_callphone", "user_created_at",
    "auth_provider"]
    list_filter = ('is_staff', 'is_consultant','is_active',)
    search_fields = ['user_fullname', 'user_email', 'user_callphone', 'user_username',]



@admin.register(PhoneOTP)
class PhoneOTPAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = PhoneOTPPropertyAdminResource
    list_display = ('user_callphone', 'otp', 'created_at', 'updated_at', 'is_used')
    list_filter = ('is_used',)
    search_fields = ['user_callphone', 'otp']
    list_per_page = 20 


@admin.register(mailVerify)
class mailVerifyAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = mailVerifyPropertyAdminResource
    list_display = ["user_id", "user_email", "created_at", "updated_at"]
    search_fields = ['user_email']
    list_per_page = 20

@admin.register(user_unmatch)
class user_unmatchAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = user_unmatchPropertyAdminResource
    list_display = ["id","user_id", "user_unmatch", "user_unmatch_created_at"]
    search_fields = ['user_id__userid']
    list_per_page = 20


# FOR REMOVE USER WITH THEIR OUTSTANDING TOKENS
class NewOutstandingTokenAdmin(OutstandingTokenAdmin):
    def has_delete_permission(self, *args, **kwargs):
        return True


admin.site.unregister(models.OutstandingToken)
admin.site.register(models.OutstandingToken, NewOutstandingTokenAdmin)

