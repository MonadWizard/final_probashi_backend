from import_export.admin import ImportExportModelAdmin
from django.contrib import admin
from .models import StaticSettingData, PromoCodeData, User_settings, Notification
from .resource import (
    PromoCodeDataPropertyAdminResource,
    StaticSettingDataPropertyAdminResource,
)


@admin.register(PromoCodeData)
class PromoCodeAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = PromoCodeDataPropertyAdminResource
    # list_display = ('promo_code', 'promo_code_point', 'promo_code_amount')


# admin.site.register(PromoCodeData, PromoCodeAdmin)


@admin.register(StaticSettingData)
class StaticSettingAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = StaticSettingDataPropertyAdminResource


# admin.site.register(StaticSettingData,StaticSettingAdmin)


admin.site.register(User_settings)
admin.site.register(Notification)
