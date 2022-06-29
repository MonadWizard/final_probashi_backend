from import_export.admin import ImportExportModelAdmin
from django.contrib import admin

from .models import (
    User_socialaccount_and_about,
    User_experience,
    User_education,
    User_idverification,
)

from .resource import (
    User_socialaccount_and_aboutPropertyAdminResource,
    User_experiencePropertyAdminResource,
    User_educationPropertyAdminResource,
    User_idverificationPropertyAdminResource,
)

# admin.site.register(User_socialaccount_and_about)
# admin.site.register(User_experience)
# admin.site.register(User_education)
# admin.site.register(User_idverification)

@admin.register(User_socialaccount_and_about)
class User_socialaccount_and_aboutAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = User_socialaccount_and_aboutPropertyAdminResource
    # list_display = ["user_fullname", "user_email", "user_callphone", "user_created_at"]

@admin.register(User_experience)
class User_experienceAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = User_experiencePropertyAdminResource
    # list_display = ["user_fullname", "user_email", "user_callphone", "user_created_at"]

@admin.register(User_education)
class User_educationAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = User_educationPropertyAdminResource
    # list_display = ["user_fullname", "user_email", "user_callphone", "user_created_at"]

@admin.register(User_idverification)
class User_idverificationAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = User_idverificationPropertyAdminResource
    # list_display = ["user_fullname", "user_email", "user_callphone", "user_created_at"]



