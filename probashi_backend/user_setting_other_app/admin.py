from import_export.admin import ImportExportModelAdmin
from django.contrib import admin
from .models import StaticSettingData, PromoCodeData
from .resource import PropertyAdminResource

@admin.register(PromoCodeData)
class PromoCodeAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = PropertyAdminResource
    # list_display = ('promo_code', 'promo_code_point', 'promo_code_amount')


# admin.site.register(PromoCodeData, PromoCodeAdmin)
admin.site.register(StaticSettingData)