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
    list_display = ["id", "userid", "userblog_title", "userblog_discription", "userblog_sharelink", "userblog_tags", "userblog_addphotopath",
    "userblog_publishlocation", "userblog_publishdate"]
    # list_filter = ('payment_status',)
    search_fields = ['id','userid__userid', 'userblog_publishlocation']
    list_per_page = 20


@admin.register(Blog_comment)
class Blog_commentAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = Blog_commentPropertyAdminResource
    list_display = ["id","userid", "blogid", "blogcomment", "blogcomment_publisherlocation"]
    search_fields = ['id','userid__userid', 'blogid__id']
    list_per_page = 20

@admin.register(Blog_reaction)
class Blog_reactionAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = Blog_reactionPropertyAdminResource
    list_display = ["id","userid", "blogid", "is_user_like", "is_user_dislike"]
    list_filter = ('is_user_like','is_user_dislike')
    search_fields = ['id','userid__userid', 'blogid__id']
    list_per_page = 20



