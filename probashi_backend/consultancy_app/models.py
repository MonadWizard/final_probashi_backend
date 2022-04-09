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
        return str(self.consultancyid) + ' ' + str(self.consultancy_timeschudile_startdate)





class UserConsultAppointmentRequest(models.Model):
    seekerid = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    # consultancy_id = models.ForeignKey(ConsultancyCreate, on_delete=models.DO_NOTHING)
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

    payment_status = models.BooleanField(default=False)   # not use yet


'''
<QueryDict: {
'tran_id': ['0410014307542609'], 
'val_id': ['22041014421pFJjZyJ0ZS2yim5'], 
'amount': ['100.00'], 
'card_type': ['BKASH-BKash'], 
'store_amount': ['97.50'], 
'card_no': [''], 
'bank_tran_id': ['220410144211jDzIGbyUMkHhcx'], 
'status': ['VALID'], 
'tran_date': ['2022-04-10 01:44:21'], 
'error': [''], 
'currency': ['BDT'], 
'card_issuer': ['BKash Mobile Banking'], 
'card_brand': ['MOBILEBANKING'], 
'card_sub_brand': ['Classic'], 
'card_issuer_country': ['Bangladesh'], 
'card_issuer_country_code': ['BD'], 
'store_id': ['mworg624bb703abfce'], 
'verify_sign': ['aa116f4aac69e862ff335b96ec75a369'], 
'verify_key': ['amount,bank_tran_id,base_fair,card_brand,card_issuer,card_issuer_country,card_issuer_country_code,card_no,card_sub_brand,card_type,currency,currency_amount,currency_rate,currency_type,error,risk_level,risk_title,status,store_amount,store_id,tran_date,tran_id,val_id,value_a,value_b,value_c,value_d'], 
'verify_sign_sha2': ['b722b4ae29d1fc02a02a59df3ab6bfc97e57cfdb8203c70cfc66d330d21880df'], 
'currency_type': [''], 
'currency_amount': [''], 
'currency_rate': [''], 
'base_fair': [''], 
'value_a': [''], 
'value_b': [''], 
'value_c': [''], 
'value_d': [''], 
'subscription_id': [''], 
'risk_level': ['0'], 
'risk_title': ['Safe']}>

'''

class ProUserPayment(models.Model):
    userid = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    tran_id = models.CharField(max_length=200, blank=True, null=True)
    val_id = models.CharField(max_length=200, blank=True, null=True)
    amount = models.CharField(max_length=200, blank=True, null=True)
    card_type = models.CharField(max_length=200, blank=True, null=True)
    store_amount = models.CharField(max_length=200, blank=True, null=True)
    card_no = models.CharField(max_length=200, blank=True, null=True)
    bank_tran_id = models.CharField(max_length=200, blank=True, null=True)
    status = models.CharField(max_length=200, blank=True, null=True)
    tran_date = models.CharField(max_length=200, blank=True, null=True)
    error = models.CharField(max_length=200, blank=True, null=True)
    currency = models.CharField(max_length=200, blank=True, null=True)
    card_issuer = models.CharField(max_length=200, blank=True, null=True)
    card_brand = models.CharField(max_length=200, blank=True, null=True)
    card_sub_brand = models.CharField(max_length=200, blank=True, null=True)
    card_issuer_country = models.CharField(max_length=200, blank=True, null=True)
    card_issuer_country_code = models.CharField(max_length=200, blank=True, null=True)
    store_id = models.CharField(max_length=200, blank=True, null=True)
    verify_sign = models.CharField(max_length=200, blank=True, null=True)
    verify_key = models.TextField(blank=True, null=True)
    verify_sign_sha2 = models.TextField(blank=True, null=True)
    currency_type = models.CharField(max_length=200, blank=True, null=True)
    currency_amount = models.CharField(max_length=200, blank=True, null=True)
    currency_rate = models.CharField(max_length=200, blank=True, null=True)
    base_fair = models.CharField(max_length=200, blank=True, null=True)
    value_a = models.CharField(max_length=200, blank=True, null=True)
    value_b = models.CharField(max_length=200, blank=True, null=True)
    value_c = models.CharField(max_length=200, blank=True, null=True)
    value_d = models.CharField(max_length=200, blank=True, null=True)
    subscription_id = models.CharField(max_length=200, blank=True, null=True)
    risk_level = models.CharField(max_length=200, blank=True, null=True)
    risk_title = models.CharField(max_length=200, blank=True, null=True)




