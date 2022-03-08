from django.db import models
from auth_user_app.models import User
from django.contrib.postgres.fields import ArrayField


# Create your models here.
class Blog(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    userblog_title = models.CharField(max_length=200, blank=True, null=True)
    userblog_discription = models.TextField(blank=True, null=True)
    userblog_sharelink = models.CharField(max_length=200, blank=True, null=True)
    userblog_tags = ArrayField(models.CharField(max_length=200), blank=True, null=True)
    userblog_addphoto = models.CharField(max_length=200, blank=True, null=True)
    userblog_publishlocation = models.CharField(max_length=200, blank=True, null=True)


class Blog_comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    blog = models.ForeignKey(Blog, on_delete=models.DO_NOTHING)
    userblog_comment = models.TextField(blank=True, null=True)
    userblog_commentpublisher_location = models.CharField(max_length=200, blank=True, null=True)
    
class Blog_reaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    userblog_reaction = models.CharField(max_length=200, blank=True, null=True)
    userblog_reactionpublisher_location = models.CharField(max_length=200, blank=True, null=True)
