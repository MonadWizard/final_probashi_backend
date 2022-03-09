from django.db import models
from auth_user_app.models import User
# Create your models here.

class ConsultancyCreate(models.Model):
    userid = models.ForeignKey(User,related_name='user_consultancy_create' ,on_delete=models.DO_NOTHING)
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
    consultant_servicelocation = models.CharField(max_length=200, blank=True, null=True)
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



