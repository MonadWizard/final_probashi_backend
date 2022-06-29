from import_export.admin import ImportExportModelAdmin
from django.contrib import admin
from .models import Blog, Blog_comment, Blog_reaction

from .resource import (
    BlogPropertyAdminResource,
    Blog_commentPropertyAdminResource,
    Blog_reactionPropertyAdminResource,
)

@admin.register(Blog)
class BlogAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = BlogPropertyAdminResource
    # list_display = ["user_fullname", "user_email", "user_callphone", "user_created_at"]

@admin.register(Blog_comment)
class Blog_commentAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = Blog_commentPropertyAdminResource
    # list_display = ["user_fullname", "user_email", "user_callphone", "user_created_at"]

@admin.register(Blog_reaction)
class Blog_reactionAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = Blog_reactionPropertyAdminResource
    # list_display = ["user_fullname", "user_email", "user_callphone", "user_created_at"]






# Register your models here.

# admin.site.register(Blog)
# admin.site.register(Blog_comment)
# admin.site.register(Blog_reaction)
