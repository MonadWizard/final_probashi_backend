from django.core.mail import EmailMessage
import threading
# from django.http import Http404
import requests

# from .models import User


class EmailThread(threading.Thread):
    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()


class Util:
    @staticmethod
    def send_email(data):
        email = EmailMessage(
            subject=data["email_subject"],
            body=data["email_body"],
            to=[data["to_email"]],
        )
        EmailThread(email).start()


class SendMessage:
    @staticmethod
    def send_message(user_callphone, data):

        url = "https://api.mobireach.com.bd/SendTextMessage?"
        headers = {"Content-Type": "application/x-www-form-urlencoded; charset=utf-8"}
        payload = {
            "Username": "psheba",
            "Password": "ProKaAfS^8#",
            "From": "PROBASHI",
            "To": user_callphone,
            "Message": data,
        }
        response = (requests.post(url, data=payload, headers=headers),)
        resp = str(response)
        # print("respons:::::::::", resp)
        return resp


# checking method


# def get_object(self, user_email):
#     try:
#         return User.objects.get(user_email__exact=user_email)
#     except User.DoesNotExist:
#         raise Http404
