from lib2to3.pgen2 import driver
from import_export.admin import ImportExportModelAdmin
from django.contrib import admin
from .models import UserFavoutireRequestSend, UserFavouriteList, FriendsSuggation

from .resource import (
    UserFavoutireRequestSendPropertyAdminResource,
    UserFavouriteListPropertyAdminResource,
    FriendsSuggationPropertyAdminResource,
)

# Register your models here.

# admin.site.register(UserFavoutireRequestSend)
# admin.site.register(UserFavouriteList)
# admin.site.register(FriendsSuggation)

@admin.register(UserFavoutireRequestSend)
class UserFavoutireRequestSendAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = UserFavoutireRequestSendPropertyAdminResource
    list_display = ["id","userid", "favourite_request_to", "is_favourite_accept", "is_favourite_reject", "favourite_request_note"]
    list_filter = ('is_favourite_accept','is_favourite_reject')
    search_fields = ['userid__user_fullname', 'favourite_request_to__user_fullname']
    list_per_page = 20

@admin.register(UserFavouriteList)
class UserFavouriteListAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = UserFavouriteListPropertyAdminResource
    list_display = ["id","userid", "favourite_userid", "is_unread", "is_Report", "is_unmatch"]
    list_filter = ('is_unread','is_Report','is_unmatch')
    search_fields = ['userid__user_fullname', 'favourite_userid__user_fullname']
    list_per_page = 20

@admin.register(FriendsSuggation)
class FriendsSuggationAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = FriendsSuggationPropertyAdminResource
    list_display = ["id","user", "location", "goals", "interest",
    "durationyear_abroad", "current_location_durationyear", "industry", "areaof_experience",
    "industry_experienceyear", "serviceholder", "selfemployed", "currentdesignation",
    "company_name", "office_address"]
    # list_filter = ('serviceholder','selfemployed')
    search_fields = ['user__user_fullname']
    list_per_page = 20

