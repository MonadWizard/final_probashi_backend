from django.db import models
from auth_user_app.models import User

class UserFavoutireRequestSend(models.Model):
    userid = models.ForeignKey(User, on_delete=models.DO_NOTHING,related_name='user_data')
    favourite_request_to = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='connection_request_to')
    is_favourite_accept = models.BooleanField(default=False)
    is_favourite_reject = models.BooleanField(default=False)
    favourite_request_note = models.TextField(blank=True, null=True)





