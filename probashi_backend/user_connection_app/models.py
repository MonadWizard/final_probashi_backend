from django.db import models
from auth_user_app.models import User

class UserConnectionRequestSend(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING,related_name='user_data')
    connection_request_to = models.ForeignKey(User, unique=True, on_delete=models.DO_NOTHING, related_name='connection_request_to')
    is_connection_accept = models.BooleanField(default=False)
    is_connection_reject = models.BooleanField(default=False)
    connection_request_note = models.TextField(blank=True, null=True)






