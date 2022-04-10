from rest_framework import serializers
# from .helper import Google, Facebook, TwitterAuthTokenVerification
from .helper import Google, Facebook, Linkedin
from .register import register_social_user
import os
from rest_framework.exceptions import AuthenticationFailed
import datetime 


class GoogleSocialAuthSerializer(serializers.Serializer):
    auth_token = serializers.CharField()

    def validate_auth_token(self, auth_token):
        user_data = Google.validate(auth_token)
        print("user_data::::", user_data)
        try:
            user_data['sub']
        except:
            raise serializers.ValidationError(
                'The token is invalid or expired. Please login again......'
            )
        googleClientID = "484261068183-vddlkf5r9oqm72stpkqvbpq874sv98a5.apps.googleusercontent.com"
        # print("user_data['aud']::::",user_data)
        if user_data['aud'] != googleClientID :
            raise AuthenticationFailed('oops, who are you?')
        userid = user_data['sub']

        user_email = user_data['email']
        user_fullname = user_data['name']
        provider = 'google'

        return register_social_user(
            provider=provider, user_email=user_email, user_fullname=user_fullname)




class FacebookSocialAuthSerializer(serializers.Serializer):
    """Handles serialization of facebook related data"""
    auth_token = serializers.CharField()

    def validate_auth_token(self, auth_token):
        
        user_data = Facebook.validate(auth_token)

        try:
            # user_id = user_data['id']
            user_email = user_data['email']
            user_fullname = user_data['name']
            provider = 'facebook'
            return register_social_user(
                provider=provider,
                # user_id=user_id,
                user_email=user_email,
                user_fullname=user_fullname
            )
        except Exception as identifier:

            raise serializers.ValidationError(
                'The token  is invalid or expired. Please login again.'
            )


class LinkedinSocialAuthSerializer(serializers.Serializer):
    """Handles serialization of linkedin related data"""
    auth_token = serializers.CharField()

    def validate_auth_token(self, auth_token):
        # print("user_data::::",auth_token)
        user_data = Linkedin.validate(auth_token)

        try:
            user_email = user_data['email']
            user_fullname = user_data['name']
            provider = 'linkedin'
            return register_social_user(
                provider=provider,
                user_email=user_email,
                user_fullname=user_fullname
            )
        except Exception as identifier:

            raise serializers.ValidationError(
                'The token  is invalid or expired. Please login again.'
            )

