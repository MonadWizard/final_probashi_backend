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


@admin.register(User_socialaccount_and_about)
class User_socialaccount_and_aboutAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = User_socialaccount_and_aboutPropertyAdminResource
    list_display = ["id", "userid", "user_about", "user_fbaccount", "user_twitteraccount","user_instagramaccount","user_linkedinaccount",
    "user_website", "user_whatsapp_account", "user_whatsapp_visibility", "user_viber_account", "user_viber_visibility", "user_immo_account", "user_immo_visibility"]
    # list_filter = ["user_whatsapp_visibility","user_viber_visibility","user_immo_visibility"]
    search_fields = ["userid__userid"]

@admin.register(User_experience)
class User_experienceAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = User_experiencePropertyAdminResource
    list_display = ["id", "userid", "user_designation", "user_companyname", "user_responsibilities","userexperience_startdate","userexperience_enddate"]
    # list_filter = ["userexperience_startdate","userexperience_enddate"]
    search_fields = ["userid__userid"]

@admin.register(User_education)
class User_educationAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = User_educationPropertyAdminResource
    list_display = ["id", "userid", "user_edu_degree", "user_edu_institutename", "user_edu_startdate", "user_edu_enddate"]
    # list_filter = ["user_edu_startdate","user_edu_enddate"]
    search_fields = ["userid__userid"]
@admin.register(User_idverification)
class User_idverificationAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = User_idverificationPropertyAdminResource
    list_display = ["id", "userid", "is_user_permanent_resident", "user_verify_id_type", "user_verify_passportphoto_path"]
    # list_filter = ["user_edu_startdate","user_edu_enddate"]
    search_fields = ["userid__userid"]


