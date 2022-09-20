from tabnanny import verbose
from django.db import models
from auth_user_app.models import User
from django.contrib.postgres.fields import ArrayField


class UserFavoutireRequestSend(models.Model):
    userid = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_data")
    favourite_request_to = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="connection_request_to"
    )
    is_favourite_accept = models.BooleanField(default=False)
    is_favourite_reject = models.BooleanField(default=False)
    favourite_request_note = models.TextField(blank=True, null=True)
    
    def __str__(self):  
        return str(self.userid) if self.userid else "userid is none"

    class Meta:
        verbose_name = "User Favorite request send"
        verbose_name_plural = "User Favorite request sends"





class UserFavouriteList(models.Model):
    userid = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="login_user_data"
    )
    favourite_userid = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="friend_user_data"
    )
    is_unread = models.BooleanField(default=False)
    is_Report = models.BooleanField(default=False)
    is_unmatch = models.BooleanField(default=False)

    def __str__(self):
        return (
            str(self.userid.user_fullname) if self.userid else "user_fullname is none"
        )
    class Meta:
        verbose_name = "User Favorite list"
        verbose_name_plural = "User Favorite lists"


# -------------------X----------------------------friend matching-------------------------------X-----------------

# location ,
class FriendsSuggation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    location = ArrayField(models.CharField(max_length=200), blank=True, null=True)
    goals = ArrayField(models.CharField(max_length=200), blank=True, null=True)
    interest = ArrayField(models.CharField(max_length=200), blank=True, null=True)
    durationyear_abroad = ArrayField(models.CharField(max_length=200), blank=True, null=True)
    current_location_durationyear = ArrayField(models.CharField(max_length=200), blank=True, null=True)
    industry = ArrayField(models.CharField(max_length=200), blank=True, null=True)
    areaof_experience = ArrayField(models.CharField(max_length=200), blank=True, null=True)
    industry_experienceyear = ArrayField(models.CharField(max_length=200), blank=True, null=True)
    serviceholder = ArrayField(models.CharField(max_length=200), blank=True, null=True)
    selfemployed = ArrayField(models.CharField(max_length=200), blank=True, null=True)
    currentdesignation = ArrayField(models.CharField(max_length=200), blank=True, null=True)
    company_name = ArrayField(models.CharField(max_length=200), blank=True, null=True)
    office_address = ArrayField(models.CharField(max_length=200), blank=True, null=True)

    def __str__(self):
        return str(self.user) if self.user else "user is none"

    class Meta:
        verbose_name = "Friends Suggestion"
        verbose_name_plural = "Friends Suggestions"
