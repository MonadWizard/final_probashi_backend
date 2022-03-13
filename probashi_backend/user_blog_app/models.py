from django.db import models
from auth_user_app.models import User
from django.contrib.postgres.fields import ArrayField


# Create your models here.
class Blog(models.Model):
    userid = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    userblog_title = models.CharField(max_length=200, blank=True, null=True)
    userblog_discription = models.TextField(blank=True, null=True)
    userblog_sharelink = models.CharField(max_length=200, blank=True, null=True)
    userblog_tags = ArrayField(models.CharField(max_length=200), blank=True, null=True)
    userblog_addphotopath = models.ImageField(upload_to='blog/post_photo', blank=True, null=True)
    userblog_publishlocation = models.CharField(max_length=200, blank=True, null=True)


class Blog_comment(models.Model):
    userid = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    blogid = models.ForeignKey(Blog, on_delete=models.DO_NOTHING)
    blogcomment = models.TextField(blank=True, null=True)
    blogcomment_publisherlocation = models.CharField(max_length=200, blank=True, null=True)
    
class Blog_reaction(models.Model):
    userid = models.ForeignKey(User, on_delete=models.CASCADE)
    blogid = models.ForeignKey(Blog, unique=True, on_delete=models.CASCADE)
    is_user_like = models.BooleanField(default=False)
    is_user_dislike = models.BooleanField(default=False)







