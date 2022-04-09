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

import json

class Facebook:

#       validate method Queries the facebook GraphAPI to fetch the user info
    @staticmethod
    def validate(auth_token):
        # print("auth token::::::::",auth_token)

        try:
            graph = facebook.GraphAPI(access_token=auth_token)
            profile = graph.request('/me?fields=name,email')

            print("profile:::::", profile)
            return profile
        except:
            return "The token is invalid or expired."


# import linkedin
import requests
from requests.structures import CaseInsensitiveDict

class Linkedin:
    @staticmethod
    def validate(auth_token):
        # print("auth_token::::",auth_token)

        try:

            url = f"https://api.linkedin.com/v2/me?oauth2_access_token={auth_token}"
            headers = CaseInsensitiveDict()
            headers["Accept"] = "*/*"
            resp_name = requests.get(url, headers=headers)
            resp_dict_name = resp_name.json()
            # print("resp_dict_name:::",resp_dict_name)
            resp_fullname = resp_dict_name['localizedFirstName'] + " " + resp_dict_name['localizedLastName']

            # print("resp_fullname:::",resp_fullname)

            url = "https://api.linkedin.com/v2/emailAddress?q=members&projection=(elements*(handle~))"
            headers = CaseInsensitiveDict()
            headers["Accept"] = "application/json"
            headers["Authorization"] = f"Bearer {auth_token}"
            resp_mail = requests.get(url, headers=headers)
            resp_dict_mail = resp_mail.json()
            resp_mail = resp_dict_mail['elements'][0]['handle~']['emailAddress']
            # print("resp:::",resp_dict_mail)
            # print(resp.status_code)

            resp_data = {'name': resp_fullname, 'email': resp_mail}
            # print("resp_data:::",resp_data)
            return resp_data

        except:
            return "The token is invalid or expired."