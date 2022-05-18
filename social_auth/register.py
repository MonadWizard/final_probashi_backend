from django.contrib.auth import authenticate
from auth_user_app.models import User
from user_connection_app.models import FriendsSuggation
import os
import random
from rest_framework.exceptions import AuthenticationFailed
import datetime
from user_profile_app.models import User_socialaccount_and_about
from user_setting_other_app.models import User_settings


def generate_username(name):

    username = "".join(name.split(" ")).lower()
    if not User.objects.filter(user_username=username).exists():
        return username
    else:
        random_username = username + str(random.randint(0, 1000))
        return generate_username(random_username)


def register_social_user(provider, user_email, user_fullname, user_image):
    filtered_user_by_email = User.objects.filter(user_email=user_email)

    if filtered_user_by_email.exists():
        # print("exist................", filtered_user_by_email[0].auth_provider)
        if filtered_user_by_email[0].is_active == True:
            if provider == filtered_user_by_email[0].auth_provider:
                social_secret = "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"
                registered_user = authenticate(
                    user_email=user_email, password=social_secret
                )

                return {
                    "user_fullname": registered_user.user_fullname,
                    "user_email": registered_user.user_email,
                    # "user_image": user_image,
                    "tokens": registered_user.tokens(),
                }

            else:
                # raise AuthenticationFailed(
                #     detail='Please continue your login using ' + filtered_user_by_email[0].auth_provider)
                return {
                    "fail": f"'Please continue your login using ' {filtered_user_by_email[0].auth_provider}"
                }
        else:
                # raise AuthenticationFailed(
                #     detail='Please continue your login using ' + filtered_user_by_email[0].auth_provider)
                return {
                    "fail": f"'inactive user ' {filtered_user_by_email[0].auth_provider}"
                }

    else:
        social_secret = "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"

        current_time = datetime.datetime.now()
        current_time = current_time.strftime("%m%d%H%M%S%f")
        userid = current_time

        user = {
            # 'username': generate_username(name), 'email': email,
            "userid": userid,
            "user_fullname": generate_username(user_fullname),
            "user_email": user_email,
            "password": social_secret,
        }
        user = User.objects.create_user(**user)
        user.is_verified = True
        user.auth_provider = provider
        user.save()

        User_socialaccount_and_about.objects.create(
            userid=User.objects.get(userid=userid),
        )
        User_settings.objects.create(
            userid=User.objects.get(userid=userid),
        )
        FriendsSuggation.objects.create(
            user=User.objects.get(userid=userid),
        )  # friend suggation .................

        new_user = authenticate(user_email=user_email, password=social_secret)
        return {
            "user_email": new_user.user_email,
            "user_fullname": new_user.user_fullname,
            "user_image": user_image,
            "tokens": new_user.tokens(),
        }
