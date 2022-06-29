from import_export.admin import ImportExportModelAdmin
from django.contrib import admin

# Register your models here.

from .models import (
    ConsultancyCreate,
    UserConsultAppointmentRequest,
    ConsultancyTimeSchudile,
    ProUserPayment,
    ConsultancyPayment,
)

from .resource import (
    ConsultancyCreatePropertyAdminResource,
    UserConsultAppointmentRequestPropertyAdminResource,
    ConsultancyTimeSchudilePropertyAdminResource,
    ProUserPaymentPropertyAdminResource,
    ConsultancyPaymentPropertyAdminResource,
)



# admin.site.register(ConsultancyCreate)
# admin.site.register(UserConsultAppointmentRequest)
# admin.site.register(ConsultancyTimeSchudile)
# admin.site.register(ProUserPayment)
# admin.site.register(ConsultancyPayment)


@admin.register(ConsultancyCreate)
class ConsultancyCreateAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = ConsultancyCreatePropertyAdminResource
    # list_display = ["user_fullname", "user_email", "user_callphone", "user_created_at"]

@admin.register(UserConsultAppointmentRequest)
class UserConsultAppointmentRequestAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = UserConsultAppointmentRequestPropertyAdminResource
    # list_display = ["user_fullname", "user_email", "user_callphone", "user_created_at"]

@admin.register(ConsultancyTimeSchudile)
class ConsultancyTimeSchudileAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = ConsultancyTimeSchudilePropertyAdminResource
    # list_display = ["user_fullname", "user_email", "user_callphone", "user_created_at"]

@admin.register(ProUserPayment)
class ProUserPaymentAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = ProUserPaymentPropertyAdminResource
    # list_display = ["user_fullname", "user_email", "user_callphone", "user_created_at"]

@admin.register(ConsultancyPayment)
class ConsultancyPaymentAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = ConsultancyPaymentPropertyAdminResource
    # list_display = ["user_fullname", "user_email", "user_callphone", "user_created_at"]






