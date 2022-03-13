from django.contrib import admin
from .models import Blog, Blog_comment,Blog_reaction
# Register your models here.

admin.site.register(Blog)
admin.site.register(Blog_comment)
admin.site.register(Blog_reaction)
