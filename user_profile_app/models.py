from django.db import models
from auth_user_app.models import User


class User_socialaccount_and_about(models.Model):
    userid = models.OneToOneField(
        User, related_name="user_socialaboutdata", on_delete=models.CASCADE
    )
    user_about = models.TextField(blank=True, null=True)
    user_fbaccount = models.CharField(max_length=200, blank=True, null=True)
    user_twitteraccount = models.CharField(max_length=200, blank=True, null=True)
    user_instagramaccount = models.CharField(max_length=200, blank=True, null=True)
    user_linkedinaccount = models.CharField(max_length=200, blank=True, null=True)
    user_website = models.CharField(max_length=200, blank=True, null=True)

    user_whatsapp_account = models.CharField(max_length=200, blank=True, null=True)
    user_whatsapp_visibility = models.CharField(max_length=20, blank=True, null=True)
    user_viber_account = models.CharField(max_length=200, blank=True, null=True)
    user_viber_visibility = models.CharField(max_length=20, blank=True, null=True)
    user_immo_account = models.CharField(max_length=200, blank=True, null=True)
    user_immo_visibility = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return str(self.userid) if self.userid else "userid is none"


class User_experience(models.Model):
    userid = models.ForeignKey(
        User, related_name="user_experiencedata", on_delete=models.CASCADE
    )
    user_designation = models.CharField(max_length=200, blank=True, null=True)
    user_companyname = models.CharField(max_length=200, blank=True, null=True)
    user_responsibilities = models.TextField(blank=True, null=True)
    userexperience_startdate = models.DateField(blank=True, null=True)
    userexperience_enddate = models.DateField(blank=True, null=True)

    def __str__(self):
        return str(self.userid) if self.userid else "userid is none"



class User_education(models.Model):
    userid = models.ForeignKey(
        User, related_name="user_educationdata", on_delete=models.CASCADE
    )
    user_edu_degree = models.CharField(max_length=200, blank=True, null=True)
    user_edu_institutename = models.CharField(max_length=200, blank=True, null=True)
    user_edu_startdate = models.DateField(blank=True, null=True)
    user_edu_enddate = models.DateField(blank=True, null=True)

    def __str__(self):
        return str(self.userid.user_email) if self.userid.user_email else "user email is none"


class User_idverification(models.Model):
    userid = models.ForeignKey(
        User, related_name="user_idverificationdata", on_delete=models.CASCADE
    )
    is_user_permanent_resident = models.BooleanField(default=False)
    user_verify_id_type = models.CharField(max_length=200, blank=True, null=True)
    user_verify_passportphoto_path = models.ImageField(
        upload_to="user/ID_verification", blank=True, null=True
    )

    def __str__(self):
        return str(self.userid) if self.userid else "userid is none"


