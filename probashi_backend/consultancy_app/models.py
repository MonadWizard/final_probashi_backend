from django.db import models
from auth_user_app.models import User
# Create your models here.

class ConsultancyCreate(models.Model):
    userid = models.ForeignKey(User,related_name='user_consultancydata', on_delete=models.DO_NOTHING)
    is_userconsultant_personal = models.BooleanField(default=False)
    is_userconsultant_company = models.BooleanField(default=False)
    consultant_name = models.CharField(max_length=200, blank=True, null=True)
    consultant_contactnumber = models.CharField(max_length=200, blank=True, null=True)
    consultant_email = models.CharField(max_length=200, blank=True, null=True)
    consultantpersonal_about = models.TextField(blank=True, null=True)
    consultantpersonal_presentaddress = models.TextField(blank=True, null=True)
    consultantpersonal_permanentaddress = models.TextField(blank=True, null=True)
    consultantcompany_primarycontract_name = models.CharField(max_length=200, blank=True, null=True)
    consultantcompany_primarycontract_number = models.CharField(max_length=200, blank=True, null=True)
    consultantcompany_primarycontract_email = models.CharField(max_length=200, blank=True, null=True)
    consultantcompany_about = models.TextField(blank=True, null=True)
    consultantcompany_reg_officeaddress = models.TextField(blank=True, null=True)
    consultantcompany_presentaddress = models.TextField(blank=True, null=True)
    consultantcompany_website = models.CharField(max_length=200, blank=True, null=True)
    consultant_company_fblink = models.CharField(max_length=200, blank=True, null=True)
    consultant_company_linkedinlink = models.CharField(max_length=200, blank=True, null=True)
    
    consultant_service_category = models.CharField(max_length=200, blank=True, null=True)
# Education Service
    educationService_degree = models.CharField(max_length=200, blank=True, null=True)
#Overseas Recruitment Service    
    overseasrecruitmentservice_job_type = models.CharField(max_length=200, blank=True, null=True)
# Medical Consultancy Service
    medicalconsultancyservice_treatment_area = models.CharField(max_length=200, blank=True, null=True)
# Legal&Civil Service
    legalcivilservice_required = models.CharField(max_length=200, blank=True, null=True)
    legalcivilservice_issue = models.CharField(max_length=200, blank=True, null=True)
# Property Management Service
    propertymanagementservice_propertylocation = models.CharField(max_length=200, blank=True, null=True)
    propertymanagementservice_type = models.CharField(max_length=200, blank=True, null=True)
    propertymanagementservice_need = models.CharField(max_length=200, blank=True, null=True)
# Tourism Service
    tourismservices = models.CharField(max_length=200, blank=True, null=True)
# Training Service
    trainingservice_topic = models.CharField(max_length=200, blank=True, null=True)
    trainingservice_duration = models.CharField(max_length=200, blank=True, null=True)
# Digital Service
    digitalservice_type = models.CharField(max_length=200, blank=True, null=True)
# Trade Facilitation Service
    tradefacilitationservice_type = models.CharField(max_length=200, blank=True, null=True)
    tradefacilitationservice_Purpose = models.CharField(max_length=200, blank=True, null=True)

    consultant_service_locationcountry = models.CharField(max_length=200, blank=True, null=True)
    consultant_servicebudget_startrange = models.IntegerField(blank=True, null=True)
    consultant_servicebudget_endrange = models.IntegerField(blank=True, null=True)
    consultant_servicedescription = models.TextField(blank=True, null=True)
    consultant_servicedetail_filepath = models.FileField(upload_to='user/consultant_servicedetail_file', blank=True, null=True)
    consultant_cvpath = models.FileField(upload_to='user/consultant_cv', blank=True, null=True)
    consultant_idverification_type = models.CharField(max_length=200, blank=True, null=True)
    consultant_idverification_passportimagepath = models.ImageField(upload_to='user/consultant_idverification_passportimage', blank=True, null=True)
    consultant_tin = models.CharField(max_length=200, blank=True, null=True)
    consultant_bin = models.CharField(max_length=200, blank=True, null=True)
    consultant_otherpermits = models.CharField(max_length=200, blank=True, null=True)
    consultant_bankaccount = models.CharField(max_length=200, blank=True, null=True)
    consultant_bankaccount_number = models.CharField(max_length=200, blank=True, null=True)
    consultant_bankaccount_branchnumber = models.CharField(max_length=200, blank=True, null=True)
    consultant_bankaccount_swiftcode = models.CharField(max_length=200, blank=True, null=True)
    consultant_bankaccount_routingnumber = models.CharField(max_length=200, blank=True, null=True)



    def __str__(self):
        return self.consultant_service_category


class ConsultancyTimeSchudile(models.Model):
    consultancyid = models.ForeignKey(ConsultancyCreate,related_name='consultancy_timeschudile', on_delete=models.DO_NOTHING)
    consultancy_timeschudile_startdate = models.DateField(blank=True, null=True)
    consultancy_starttime = models.TimeField(blank=True, null=True)
    consultancy_endtime = models.TimeField(blank=True, null=True)
    consultancy_rate = models.IntegerField(blank=True, null=True)
    is_consultancy_take = models.BooleanField(default=False)

    def __str__(self):
        return str(self.consultancy_timeschudile_startdate)





class UserConsultAppointmentRequest(models.Model):
    seekerid = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    consultancy_id = models.ForeignKey(ConsultancyCreate, on_delete=models.DO_NOTHING)
    ConsultancyTimeSchudile = models.ForeignKey(ConsultancyTimeSchudile, unique=True, on_delete=models.DO_NOTHING)
    appointment_request_datetime = models.DateTimeField(auto_now_add=True)
    # appointment_seeker_requested_datetime = models.DateTimeField()
    appointment_attendent_name = models.CharField(max_length=200, blank=True, null=True)
    appointment_seeker_cellphone = models.CharField(max_length=200, blank=True, null=True)
    appointment_seeker_email = models.CharField(max_length=200, blank=True, null=True)
    appointment_seeker_note = models.TextField(blank=True, null=True)

    appointment_seeker_starrating = models.DecimalField(max_digits=2, decimal_places=1, blank=True, null=True)
    appointment_seeker_starrating_comment = models.TextField(blank=True, null=True)

    consultant_provider_starratting = models.DecimalField(max_digits=2, decimal_places=1, blank=True, null=True)
    consultant_provider_starratting_comment = models.TextField(blank=True, null=True)

    reason_for_missing_appointment = models.TextField(blank=True, null=True)









