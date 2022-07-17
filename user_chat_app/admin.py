from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from import_export import resources
from user_chat_app.models import ChatTable

# admin.site.register(ChatTable)


class ChatTablePropertyAdminResource(resources.ModelResource):
    class Meta:
        model = ChatTable
        # exclude = ('id',)
        import_id_fields = ("id",)

@admin.register(ChatTable)
class ChatTableAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = ChatTablePropertyAdminResource
    list_display = ["id","user_1", "user_2", "table_name"]
    # list_filter = ('is_user_like','is_user_dislike')
    search_fields = ['id']
    list_per_page = 20

