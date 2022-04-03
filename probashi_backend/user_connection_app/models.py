from django.db import models
from auth_user_app.models import User

class UserFavoutireRequestSend(models.Model):
    userid = models.ForeignKey(User, on_delete=models.DO_NOTHING,related_name='user_data')
    favourite_request_to = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='connection_request_to')
    is_favourite_accept = models.BooleanField(default=False)
    is_favourite_reject = models.BooleanField(default=False)
    favourite_request_note = models.TextField(blank=True, null=True)


class UserFavouriteList(models.Model):
    userid = models.ForeignKey(User, on_delete=models.DO_NOTHING,related_name='login_user_data')
    favourite_userid = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='friend_user_data')
    is_unread = models.BooleanField(default=False)
    is_Report = models.BooleanField(default=False)
    is_unmatch = models.BooleanField(default=False)

    def __str__(self):
        return self.userid.user_fullname