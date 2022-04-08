from django.http import HttpResponse
from rest_framework import generics, status, views, permissions
from .serializers import (RegisterSerializer,
                        UpdateRegisterSerializer,
                        SetNewPasswordSerializer, 
                        ResetPasswordEmailRequestSerializer, 
                        LoginSerializer, 
                        LogoutSerializer, 
                        ViewUserSerializer,
                        InAppChangePasswordSerializer,
                        PhoneOtpRegisterSerializer,
                        PhoneLoginSerializer,
                        userOTP)

from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import permissions
from django.http import Http404

from user_setting_other_app.models import User_settings
from .models import User, PhoneOTP, FriendSuggation
from user_profile_app.models import User_socialaccount_and_about
from .utils import Util, SendMessage
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
import jwt
from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponsePermanentRedirect
import os
import datetime 
from django.db.models import Q
import random
from django.utils import timezone
# from user_chat_app.models import FriendSuggation


class MailVerifyRequestView(views.APIView):
    
    def post(self, request):
        data = request.data
        user_fullname = data['user_fullname']
        user_email = data['user_email']
        password = data['password']

        if User.objects.filter(user_email=user_email).exists():
            return Response({"message": "Email already exists"}, status=status.HTTP_400_BAD_REQUEST)
        else:
    # Token passing
            payload = {
                'user_email': user_email,
                'user_fullname': user_fullname,
                'password': password,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30, seconds=00),
                'iat': datetime.datetime.utcnow()
            }
            token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

            current_site = get_current_site(request).domain
            relativeLink = reverse('email-verify')
            absurl = 'http://'+current_site+relativeLink+"?token="+str(token)
            
            email_body = 'Hi '+user_fullname + \
                ' Use the link below to verify your email \n' + absurl
            
            data = {'email_body': email_body, 'to_email': user_email,
                    'email_subject': 'Verify your email'}
            # print('data:', data)

            Util.send_email(data)

            return Response(data, status=status.HTTP_200_OK)


class VerifyEmail(views.APIView):

    serializer_class = RegisterSerializer

    def get(self, request):
        token = request.GET.get('token')

        try:
            verified_mail_payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])

            current_time = datetime.datetime.now() 
            current_time = current_time.strftime("%m%d%H%M%S%f")
            
            userid = current_time
            verified_mail_payload["userid"]= userid

            serializer = self.serializer_class(data=verified_mail_payload)
            serializer.is_valid(raise_exception=True)

            serializer.save()

            User_socialaccount_and_about.objects.create(userid=User.objects.get(userid=userid), )
            User_settings.objects.create(userid=User.objects.get(userid=userid), )
            FriendSuggation.objects.create(user=User.objects.get(userid=userid), )
            

            html = "<html><body>Verification Success. It's time for complete registration.</body></html>"
            return HttpResponse(html)
        except jwt.ExpiredSignatureError as identifier:
            html = "<html><body>Activation Expired.</body></html>"
            return HttpResponse(html)
        except jwt.exceptions.DecodeError as identifier:
            html = "<html><body>Invalid token.</body></html>"
            return HttpResponse(html)


class MailVerificationStatus(views.APIView):
    def get(self,request):
        user_mail = User.objects.filter(user_email__exact=request.data['user_email'])
        mail_verify = user_mail.values('is_verified')
        return Response(mail_verify, status=status.HTTP_200_OK)


class UpdateRegisterView(views.APIView):


    def get_object(self,user_email):
        try:
            return User.objects.get(user_email__exact=user_email)
        except User.DoesNotExist:
            raise Http404

    def get(self,request,user_email):
        user_email = self.get_object(user_email)
        serializer = UpdateRegisterSerializer(user_email)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def put(self,request,user_email):
        user_email = self.get_object(user_email)
        fullname_pasport = request.data['user_fullname_passport']
        serializer = UpdateRegisterSerializer(user_email,data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        
        # relativeLink = reverse('email-verify')
        email_body = 'Hi '+fullname_pasport + \
            ' welcome to probashi.. \n'
        data = {'email_body': email_body, 'to_email': user_email,
                'email_subject': 'welcome to probashi'}
        # print('data:::::::::', data)

        Util.send_email(data)
        return Response(user_data, status=status.HTTP_200_OK)
    


class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        



class RequestPasswordResetEmail(generics.GenericAPIView):

    def post(self, request):

        user_email = request.data.get('user_email', '')
        otp = request.data.get('otp', '')

        if User.objects.filter(user_email=user_email).exists():
            user = User.objects.get(user_email=user_email)
            
            # print('otp:', otp)
            

            email_body = f'''Hello,{user.user_fullname} \n code for reset password is {otp}'''
            
            data = {'email_body': email_body, 'to_email': user.user_email,
                    'email_subject': 'Reset your passsword'}
            Util.send_email(data)
        return Response({'success': 'We have sent you a link to reset your password'}, status=status.HTTP_200_OK)



class SetNewPasswordAPIView(generics.UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = SetNewPasswordSerializer
    model = User

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():            
            self.object.set_password(serializer.data.get("new_password"))
            self.object.userid = request.data.get("userid")
            self.object.save()
            # serializer.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': serializer.data,
            }

            return Response(response)

        return Response('Bad Request', status=status.HTTP_400_BAD_REQUEST)


class LogoutAPIView(generics.GenericAPIView):
    serializer_class = LogoutSerializer

    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response('logout success',status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    
class ViewUser(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ViewUserSerializer

    def get_queryset(self):
            user = self.request.user
            return User.objects.filter(userid=user.userid)



class InAppChangePassword(generics.UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = InAppChangePasswordSerializer
    model = User

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            print(request.data['old_password'])
            print('old password::::', self.object.check_password(request.data['old_password']))
            if not self.object.check_password(request.data['old_password']):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            self.object.set_password(serializer.data.get("new_password"))
            self.object.user_email = request.data.get("user_email")
            self.object.save()
            # serializer.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': serializer.data,
            }

            return Response(response)

        return Response('Bad Request', status=status.HTTP_400_BAD_REQUEST)


# --------------------x --------------x --------------x --------------x

class RegistrationVerificationCodeSend(views.APIView):
    serializer_class = userOTP

    def post(self, request):
        data = request.data
        user_fullname = data['user_fullname']
        user_callphone = data['user_callphone']
        # password = data['password']
        otp = random.sample(range(0, 9), 4)
        otp = ''.join(map(str, otp))
        data['otp'] = otp
        # print('::::::', request.data)

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()



        # print('serializer::::::::::', serializer.data)

        data = {f'''প্রিয় {user_fullname}, আপনার ভেরিফিকেশন কোডটি {otp}'''}
        # print('data:', data)

        SendMessage.send_message(user_callphone,data)

        return Response(serializer.data, status=status.HTTP_200_OK)


class PhoneNumberRegistration(views.APIView):
    serializer_class = PhoneOtpRegisterSerializer

    def post(self, request):
        current_time = datetime.datetime.now() 
        current_time = current_time.strftime("%m%d%H%M%S%f")
        userid = current_time
        request.data["userid"]= userid
        # request.data["password"]= userid

        time = timezone.localtime()
        # print('time:::', time)
        # print("::::::::::::", PhoneOTP.objects.filter(Q(user_callphone=request.data['user_callphone']) & Q(otp=request.data['otp']) & Q(updated_at__gt=time)).exists())
        if PhoneOTP.objects.filter(Q(user_callphone=request.data['user_callphone']) & Q(otp=request.data['otp']) & Q(updated_at__gt=time)).exists():
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            PhoneOTP.objects.filter(otp=request.data['otp']).update(is_used=True)
            User_socialaccount_and_about.objects.create(userid=User.objects.get(userid=userid), )
            User_settings.objects.create(userid=User.objects.get(userid=userid), )
            PhoneOTP.objects.filter(Q(is_used=True) | Q(updated_at__lt=time)).delete()
            

            return Response(request.data, status=status.HTTP_200_OK)
        return Response("Bad Request", status=status.HTTP_400_BAD_REQUEST)


class LoginVerificationCodeSend(views.APIView):
    serializer_class = userOTP

    def post(self, request):
        data = request.data
        # user_fullname = data['user_fullname']
        user_callphone = data['user_callphone']
        # password = data['password']
        otp = random.sample(range(0, 9), 4)
        otp = ''.join(map(str, otp))
        data['otp'] = otp
        user_fullname = User.objects.filter(user_callphone=user_callphone).values('user_fullname').first()
        user_fullname = user_fullname['user_fullname']
        data['user_fullname'] = user_fullname

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        data = {f'''প্রিয় {user_fullname}, আপনার ভেরিফিকেশন কোডটি {otp}'''}
        # print('data:', data)

        SendMessage.send_message(user_callphone,data)

        return Response(serializer.data, status=status.HTTP_200_OK)




# VerificationCodeSend also works for loging  
class PhoneNumberLogin(views.APIView):
    serializer_class = PhoneLoginSerializer

    def post(self, request):
        # print('request.data:', request.data)
        
        time = timezone.localtime()
        # print('time:::', PhoneOTP.objects.filter(Q(user_callphone=request.data['user_callphone']) & Q(otp=request.data['otp']) & Q(updated_at__gt=time)).exists())
        if PhoneOTP.objects.filter(Q(user_callphone=request.data['user_callphone']) & Q(otp=request.data['otp']) & Q(updated_at__gt=time)).exists():
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            
            PhoneOTP.objects.filter(otp=request.data['otp']).update(is_used=True)
            PhoneOTP.objects.filter(Q(is_used=True) | Q(updated_at__lt=time)).delete()

            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response("Bad Request", status=status.HTTP_400_BAD_REQUEST)




class PhoneUpdateRegisterView(views.APIView):


    def get_object(self,user_callphone):
        try:
            return User.objects.get(user_callphone__exact=user_callphone)
        except User.DoesNotExist:
            raise Http404

    def get(self,request,user_callphone):
        user_callphone = self.get_object(user_callphone)
        serializer = UpdateRegisterSerializer(user_callphone)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def put(self,request,user_callphone):
        user_callphone = self.get_object(user_callphone)
        fullname_pasport = request.data['user_fullname_passport']
        serializer = UpdateRegisterSerializer(user_callphone,data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        
        # relativeLink = reverse('email-verify')
        email_body = 'Hi '+fullname_pasport + \
            ' welcome to probashi.. \n'
        data = {'email_body': email_body, 'to_email': user_callphone,
                'email_subject': 'welcome to probashi'}
        # print('data:::::::::', data)

        # Util.send_email(data)
        return Response(user_data, status=status.HTTP_200_OK)
    









