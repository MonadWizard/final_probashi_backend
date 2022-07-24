from django.db.models.signals import pre_delete
from .models import User
from django.dispatch import receiver
from user_connection_app.models import FriendsSuggation


@receiver(pre_delete, sender=User)
def post_delete_action(sender, **kwargs):

    user = kwargs["instance"]

    user_id = [str(user.userid)]

    fields = [
        "location",
        "goals",
        "interest",
        "durationyear_abroad",
        "current_location_durationyear",
        "industry",
        "areaof_experience",
        "industry_experienceyear",
        "serviceholder",
        "selfemployed",
        "currentdesignation",
        "company_name",
        "office_address",
    ]
    for field in fields:
        filterr = f"{field}__overlap"
        dlt_field = FriendsSuggation.objects.filter(**{filterr: user_id}).values()
        if dlt_field:
            for u in dlt_field:
                u[f"{field}"].remove(user_id[0])
                terget_user = FriendsSuggation.objects.get(id=u["id"])
                terget_user.__dict__[field] = u[f"{field}"]
                terget_user.save()

    FriendsSuggation.objects.filter(user=user).delete()
