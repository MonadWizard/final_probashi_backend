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
    # list_display = ["user_fullname", "user_email", "user_callphone", "user_created_at"]


@admin.register(UserFavouriteList)
class UserFavouriteListAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = UserFavouriteListPropertyAdminResource
    # list_display = ["user_fullname", "user_email", "user_callphone", "user_created_at"]


@admin.register(FriendsSuggation)
class FriendsSuggationAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = FriendsSuggationPropertyAdminResource
    # list_display = ["user_fullname", "user_email", "user_callphone", "user_created_at"]

