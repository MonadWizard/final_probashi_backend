from django.db.models.signals import post_delete
from .models import User
from django.dispatch import receiver


@receiver(post_delete, sender=User)
def post_delete_action(sender, **kwargs):

    print("post_delete_action.................")
    user = kwargs["instance"]
    print("kwargs:::::::::::::::", user.userid)
