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
    list_display = ["promo_code", "promo_code_point", "promo_code_amount", "is_promo_code_active"]
    list_filter = ('promo_code_point','is_promo_code_active')
    search_fields = ['promo_code']
    list_per_page = 20

# admin.site.register(PromoCodeData, PromoCodeAdmin)


@admin.register(StaticSettingData)
class StaticSettingAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = StaticSettingDataPropertyAdminResource
    list_display = ["id", "user_industry_data", "user_current_designation", "user_areaof_experience_data", "user_interested_area_data", "user_goal_data",
                    "consultancyservice_category_data", "blog_tags_data", "user_education_data", "faq_title",
                    "privacypolicy_title", "educationService_degree", "overseasrecruitmentservice_job_type",
                    "medicalconsultancyservice_treatment_area", "legalcivilservice_required",
                    "legalcivilservice_issue", "propertymanagementservice_propertylocation",
                    "propertymanagementservice_type", "propertymanagementservice_need", "tourismservices",
                    "trainingservice_topic", "trainingservice_duration", "digitalservice_type",
                    "tradefacilitationservice_type", "tradefacilitationservice_Purpose", "country_name"]
    # list_filter = ('is_consultancy_take',)
    # search_fields = ['userid', 'consultancy_sheduleid']
    list_per_page = 20

# admin.site.register(StaticSettingData,StaticSettingAdmin)


# admin.site.register(User_settings)
# admin.site.register(Notification)
# admin.site.register(Facing_trouble)


@admin.register(User_settings)
class User_settingsAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = User_settingsPropertyAdminResource
    list_display = ["id", "userid", "user_mail_notification_enable", "user_monthly_newsleter_enable", "user_reward_point"]
    search_fields = ('userid__userid',)
    list_filter = ['user_mail_notification_enable', 'user_monthly_newsleter_enable']
    list_per_page = 20

@admin.register(Notification)
class NotificationAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = NotificationPropertyAdminResource
    list_display = ["id", "userid", "receiverid", "notification_title", "notification_description", "is_notification_seen",
                    "notification_date","is_notification_delete"]
    list_filter = ('is_notification_seen',)
    search_fields = ['userid__userid', 'receiverid__userid']
    list_per_page = 20



@admin.register(Facing_trouble)
class Facing_troubleAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = Facing_troublePropertyAdminResource
    list_display = ["id", "user", "user_problem_message", "user_problem_photo_path"]
    # # list_filter = ('is_consultancy_take',)
    search_fields = ['user__userid']
    list_per_page = 20


