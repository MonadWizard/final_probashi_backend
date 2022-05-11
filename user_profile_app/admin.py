from django.contrib import admin

from .models import (
    User_socialaccount_and_about,
    User_experience,
    User_education,
    User_idverification,
)


admin.site.register(User_socialaccount_and_about)
admin.site.register(User_experience)
admin.site.register(User_education)
admin.site.register(User_idverification)
