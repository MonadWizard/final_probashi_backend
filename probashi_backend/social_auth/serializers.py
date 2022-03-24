from rest_framework import serializers
# from .helper import Google, Facebook, TwitterAuthTokenVerification
from .helper import Google, Facebook
from .register import register_social_user
import os
from rest_framework.exceptions import AuthenticationFailed



class GoogleSocialAuthSerializer(serializers.Serializer):
    auth_token = serializers.CharField()

    def validate_auth_token(self, auth_token):
        user_data = Google.validate(auth_token)
        try:
            user_data['sub']
        except:
            raise serializers.ValidationError(
                'The token is invalid or expired. Please login again.'
            )
        googleClientID = '484261068183-vddlkf5r9oqm72stpkqvbpq874sv98a5.apps.googleusercontent.com'
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
            user_id = user_data['id']
            email = user_data['email']
            name = user_data['name']
            provider = 'facebook'
            return register_social_user(
                provider=provider,
                user_id=user_id,
                email=email,
                name=name
            )
        except Exception as identifier:

            raise serializers.ValidationError(
                'The token  is invalid or expired. Please login again.'
            )



