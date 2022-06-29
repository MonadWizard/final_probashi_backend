from import_export.admin import ImportExportModelAdmin
from django.contrib import admin
from .models import (
    StaticSettingData,
    PromoCodeData,
    User_settings,
    Notification,
    Facing_trouble,
)
from .resource import (
    PromoCodeDataPropertyAdminResource,
    StaticSettingDataPropertyAdminResource,
    User_settingsPropertyAdminResource,
    NotificationPropertyAdminResource,
    Facing_troublePropertyAdminResource,
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


# admin.site.register(User_settings)
# admin.site.register(Notification)
# admin.site.register(Facing_trouble)


@admin.register(User_settings)
class User_settingsAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = User_settingsPropertyAdminResource


@admin.register(Notification)
class NotificationAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = NotificationPropertyAdminResource


@admin.register(Facing_trouble)
class Facing_troubleAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = Facing_troublePropertyAdminResource



