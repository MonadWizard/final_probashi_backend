from django.db import models
from auth_user_app.models import User


class User_socialaccount_and_about(models.Model):
    userid = models.OneToOneField(User, on_delete=models.DO_NOTHING)
    user_about = models.TextField(blank=True, null=True)
    user_fbaccount = models.CharField(max_length=200, blank=True, null=True)
    user_twitteraccount = models.CharField(max_length=200, blank=True, null=True)
    user_instagramaccount = models.CharField(max_length=200, blank=True, null=True)
    user_linkedinaccount = models.CharField(max_length=200, blank=True, null=True)
    user_website = models.CharField(max_length=200, blank=True, null=True)

    user_whatsapp_account = models.CharField(max_length=200, blank=True, null=True)
    user_whatsapp_visibility = models.CharField(max_length=20, blank=True, null=True)
    user_viber_account = models.CharField(max_length=200, blank=True, null=True)
    user_immo_account = models.CharField(max_length=200, blank=True, null=True)


class User_experience(models.Model):
    userid = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    user_designation = models.CharField(max_length=200, blank=True, null=True)
    user_companyname = models.CharField(max_length=200, blank=True, null=True)
    user_responsibilities = models.TextField(blank=True, null=True)
    userexperience_startdate = models.DateField(blank=True, null=True)
    userexperience_enddate = models.DateField(blank=True, null=True)
    

class User_education(models.Model):
    userid = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    user_edu_degree = models.CharField(max_length=200, blank=True, null=True)
    user_edu_institutename = models.CharField(max_length=200, blank=True, null=True)
    user_edu_startdate = models.DateField(blank=True, null=True)
    user_edu_enddate = models.DateField(blank=True, null=True)
    

class User_idverification(models.Model):
    userid = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    is_user_permanent_resident = models.BooleanField(default=False)
    user_verify_id_type = models.CharField(max_length=200, blank=True, null=True)
    user_verify_passportphoto_path= models.CharField(max_length=200, blank=True, null=True)
    



