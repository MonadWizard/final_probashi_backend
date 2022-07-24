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




@admin.register(ConsultancyCreate)
class ConsultancyCreateAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = ConsultancyCreatePropertyAdminResource
    list_display = ["id","userid", "is_userconsultant_personal", "is_userconsultant_company", "consultant_name",
    "consultant_contactnumber", "consultant_email", "consultantpersonal_about", "consultantpersonal_presentaddress",
    "consultantpersonal_permanentaddress","consultantcompany_primarycontract_name", "consultantcompany_primarycontract_number",
    "consultantcompany_primarycontract_email", "consultantcompany_about", "consultantcompany_reg_officeaddress",
    "consultantcompany_presentaddress", "consultantcompany_website", "consultant_company_fblink", "consultant_company_linkedinlink",
    "consultant_service_category", "educationService_degree", "overseasrecruitmentservice_job_type", "medicalconsultancyservice_treatment_area",
    "legalcivilservice_required", "legalcivilservice_issue", "propertymanagementservice_propertylocation", "propertymanagementservice_type",
    "propertymanagementservice_need", "tourismservices", "trainingservice_topic", "trainingservice_duration", "digitalservice_type",
    "tradefacilitationservice_type", "tradefacilitationservice_Purpose", "consultant_service_locationcountry", "consultant_servicebudget_startrange",
    "consultant_servicebudget_endrange", "consultant_servicedescription", "consultant_servicedetail_filepath", "consultant_cvpath",
    "consultant_idverification_type", "consultant_idverification_passportimagepath", "consultant_tin", "consultant_bin", "consultant_otherpermits",
    "consultant_bankaccount", "consultant_bankaccount_number", "consultant_bankaccount_branchnumber", "consultant_bankaccount_swiftcode",
    "consultant_bankaccount_routingnumber", "consultant_created_at"]
    list_filter = ('consultant_service_category','is_userconsultant_personal', 'is_userconsultant_company')
    search_fields = ['id','userid__userid','consultant_name']
    list_per_page = 20

@admin.register(UserConsultAppointmentRequest)
class UserConsultAppointmentRequestAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = UserConsultAppointmentRequestPropertyAdminResource
    list_display = ["id","seekerid", "ConsultancyTimeSchudile", "appointment_request_datetime", "appointment_attendent_name", "appointment_seeker_cellphone",
    "appointment_seeker_email", "appointment_seeker_note", "appointment_seeker_starrating", "appointment_seeker_starrating_comment", 
    "consultant_provider_starratting", "consultant_provider_starratting_comment", "reason_for_missing_appointment", "payment_status"]
    list_filter = ('payment_status',)
    search_fields = ['id','appointment_seeker_email', 'seekerid__userid','appointment_attendent_name']
    list_per_page = 20



@admin.register(ConsultancyTimeSchudile)
class ConsultancyTimeSchudileAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = ConsultancyTimeSchudilePropertyAdminResource
    list_display = ["consultancyid", "consultancy_timeschudile_startdate", "consultancy_starttime", "consultancy_endtime",
    "consultancy_rate", "is_consultancy_take"]
    list_filter = ('is_consultancy_take',)
    search_fields = ['consultancyid__id', 'consultancy_rate']
    list_per_page = 20

@admin.register(ProUserPayment)
class ProUserPaymentAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = ProUserPaymentPropertyAdminResource
    list_display = ["id","userid", "tran_id", "payment_details"]
    search_fields = ['userid__userid', 'tran_id']
    list_per_page = 20

@admin.register(ConsultancyPayment)
class ConsultancyPaymentAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = ConsultancyPaymentPropertyAdminResource
    list_display = ["id","userid", "consultancy_sheduleid", "tran_id", "payment_details"]
    search_fields = ['userid__userid', 'consultancy_sheduleid__id', 'tran_id']
    list_per_page = 20





