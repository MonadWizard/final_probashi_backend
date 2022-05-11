from lib2to3.pgen2 import driver
from django.contrib import admin
from .models import UserFavoutireRequestSend, UserFavouriteList, FriendsSuggation

# Register your models here.

admin.site.register(UserFavoutireRequestSend)
admin.site.register(UserFavouriteList)
admin.site.register(FriendsSuggation)
