from django.db import models
from auth_user_app.models import User
# Create your models here.

# location , 
class FriendSuggation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # friend = models.ForeignKey('User', on_delete=models.CASCADE, related_name='friend')
    # status = models.CharField(max_length=10)
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)goal
    localtion = models.TextField()
    goals = models.TextField()
    interest = models.TextField()


    # def __str__(self):
    #     return self.user



