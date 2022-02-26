from django.contrib import admin

from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ['user_fullname', 'user_email', 'user_created_at']


admin.site.register(User, UserAdmin)