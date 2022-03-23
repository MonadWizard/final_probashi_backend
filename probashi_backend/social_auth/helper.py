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




import facebook

class Facebook:

#       validate method Queries the facebook GraphAPI to fetch the user info
    @staticmethod
    def validate(auth_token):

        try:
            graph = facebook.GraphAPI(access_token=auth_token)
            profile = graph.request('/me?fields=name,email')
            return profile
        except:
            return "The token is invalid or expired."






