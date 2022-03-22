
from django.contrib.auth import authenticate
from auth_user_app.models import User
import os
import random
from rest_framework.exceptions import AuthenticationFailed
import datetime 


def generate_username(name):

    username = "".join(name.split(' ')).lower()
    if not User.objects.filter(user_username=username).exists():
        return username
    else:
        random_username = username + str(random.randint(0, 1000))
        return generate_username(random_username)


def register_social_user(provider, user_email, user_fullname):
    filtered_user_by_email = User.objects.filter(user_email=user_email)

    if filtered_user_by_email.exists():

        if provider == filtered_user_by_email[0].auth_provider:
            social_secret = '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'
            registered_user = authenticate(
                user_email=user_email, password=social_secret)

            return {
                'user_fullname': registered_user.user_fullname,
                'user_email': registered_user.user_email,
                'tokens': registered_user.tokens()}

        else:
            raise AuthenticationFailed(
                detail='Please continue your login using ' + filtered_user_by_email[0].auth_provider)

    else:
        social_secret = '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'

        current_time = datetime.datetime.now() 
        current_time = current_time.strftime("%m%d%H%M%S%f")
        userid = current_time


        user = {
            # 'username': generate_username(name), 'email': email,
            'userid': userid,
            'user_fullname': generate_username(user_fullname), 
            'user_email': user_email,
            'password': social_secret}
        user = User.objects.create_user(**user)
        user.is_verified = True
        user.auth_provider = provider
        user.save()

        new_user = authenticate(
            user_email=user_email, password=social_secret)
        return {
            'user_email': new_user.user_email,
            'user_fullname': new_user.user_fullname,
            'tokens': new_user.tokens()
        }
