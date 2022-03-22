from google.auth.transport import requests
from google.oauth2 import id_token


class Google:
    """Google class to fetch the user info and return it"""

        # validate method Queries the Google oAUTH2 api to fetch the user info
    @staticmethod
    def validate(auth_token):
        try:
            idinfo = id_token.verify_oauth2_token(
                auth_token, requests.Request())

            if 'accounts.google.com' in idinfo['iss']:
                return idinfo

        except:
            return "The token is either invalid or has expired"




# import facebook

# class Facebook:
#     """
#     Facebook class to fetch the user info and return it
#     """

#     @staticmethod
#     def validate(auth_token):
#         """
#         validate method Queries the facebook GraphAPI to fetch the user info
#         """
#         try:
#             graph = facebook.GraphAPI(access_token=auth_token)
#             profile = graph.request('/me?fields=name,email')
#             return profile
#         except:
#             return "The token is invalid or expired."






# import twitter
# import os
# from rest_framework import serializers

# class TwitterAuthTokenVerification:
#     """
#     class to decode user access_token and user access_token_secret
#     tokens will combine the user access_token and access_token_secret
#     separated by space
#     """

#     @staticmethod
#     def validate_twitter_auth_tokens(access_token_key, access_token_secret):
#         """
#         validate_twitter_auth_tokens methods returns a twitter
#         user profile info
#         """

#         consumer_api_key = os.environ.get('TWITTER_API_KEY')
#         consumer_api_secret_key = os.environ.get('TWITTER_CONSUMER_SECRET')

#         try:
#             api = twitter.Api(
#                 consumer_key=consumer_api_key,
#                 consumer_secret=consumer_api_secret_key,
#                 access_token_key=access_token_key,
#                 access_token_secret=access_token_secret
#             )

#             user_profile_info = api.VerifyCredentials(include_email=True)
#             return user_profile_info.__dict__

#         except Exception as identifier:

#             raise serializers.ValidationError({
#                 "tokens": ["The tokens are invalid or expired"]})

