from django.db import models
from auth_user_app.models import User

class User_consultant(models.Model):
    user = models.OneToOneField(User, on_delete=models.DO_NOTHING)
    userconsultant_type= models.CharField(max_length=200, blank=True, null=True)
    userconsultant_name = models.CharField(max_length=200, blank=True, null=True)
    userconsultant_contactnumber = models.CharField(max_length=200, blank=True, null=True)
    userconsultant_email = models.CharField(max_length=200, blank=True, null=True)
    userconsultant_about = models.TextField(blank=True, null=True)
    userconsultant_presentaddress = models.TextField(blank=True, null=True)
    userconsultant_permanentaddress = models.TextField(blank=True, null=True)
    userconsultant_primary_contractname = models.CharField(max_length=200, blank=True, null=True)
    userconsultant_primary_contractnumber = models.CharField(max_length=200, blank=True, null=True)
    userconsultant_primary_email = models.CharField(max_length=200, blank=True, null=True)
    userconsultant_registered_officeaddress = models.TextField(blank=True, null=True)
    userconsultant_company_website = models.CharField(max_length=200, blank=True, null=True)
    userconsultant_fblink = models.CharField(max_length=200, blank=True, null=True)
    userconsultant_linkedinlink = models.CharField(max_length=200, blank=True, null=True)
    userconsultant_service_category = models.CharField(max_length=200, blank=True, null=True)
    userconsultant_servicelocation = models.CharField(max_length=200, blank=True, null=True)
    userconsultant_servicebudget_startrange = models.IntegerField(blank=True, null=True)
    userconsultant_servicebudget_endrange = models.IntegerField(blank=True, null=True)
    userconsultant_servicedescription = models.TextField(blank=True, null=True)
    userconsultant_servicedetail_filepath = models.CharField(max_length=200, blank=True, null=True)
    userconsultant_cvpath = models.CharField(max_length=200, blank=True, null=True)
    userconsultant_idverification_type = models.CharField(max_length=200, blank=True, null=True)
    userconsultant_idverification_pasportimagepath = models.CharField(max_length=200, blank=True, null=True)
    userconsultant_TIN = models.CharField(max_length=200, blank=True, null=True)
    userconsultant_BIN = models.CharField(max_length=200, blank=True, null=True)
    userconsultant_otherpermits = models.CharField(max_length=200, blank=True, null=True)
    userconsultant_bankaccount = models.CharField(max_length=200, blank=True, null=True)
    userconsultant_bankaccount_number = models.CharField(max_length=200, blank=True, null=True)
    userconsultant_bankaccount_branchnumber = models.CharField(max_length=200, blank=True, null=True)
    userconsultant_bankaccount_swiftcode = models.CharField(max_length=200, blank=True, null=True)
    userconsultant_bankaccount_routingnumber = models.CharField(max_length=200, blank=True, null=True)


class user_consult_appointment(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    user_consultant_pk = models.ForeignKey(User_consultant, on_delete=models.DO_NOTHING)
    appointment_request_datetime = models.DateTimeField(auto_now_add=True)
    appointment_seeker_requested_datetime = models.DateTimeField()
    appointment_attendent_name = models.CharField(max_length=200, blank=True, null=True)
    appointment_seeker_cellphone = models.CharField(max_length=200, blank=True, null=True)
    appointment_seeker_email = models.CharField(max_length=200, blank=True, null=True)
    appointment_seeker_note = models.TextField(blank=True, null=True)









