from urllib import request
from django.http import HttpResponse
from rest_framework import generics, status, views, permissions
from .serializers import (RegisterSerializer,
                        UpdateRegisterSerializer,
                        SetNewPasswordSerializer, 
                        ResetPasswordEmailRequestSerializer, 
                        LoginSerializer, 
                        LogoutSerializer, 
                        ViewUserSerializer,
                        InAppChangePasswordSerializer)

from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import permissions
from django.http import Http404

from .models import User
from user_profile_app.models import User_socialaccount_and_about
from .utils import Util
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



class MailVerifyRequestView(views.APIView):
    
    def post(self, request):
        data = request.data
        user_fullname = data['user_fullname']
        user_email = data['user_email']
        password = data['password']


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
    serializer_class = ResetPasswordEmailRequestSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        user_email = request.data.get('user_email', '')

        if User.objects.filter(user_email=user_email).exists():
            user = User.objects.get(user_email=user_email)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.userid))
            token = PasswordResetTokenGenerator().make_token(user)
            current_site = get_current_site(
                request=request).domain
            relativeLink = reverse(
                'password-reset-confirm', kwargs={'uidb64': uidb64, 'token': token})

            redirect_url = request.data.get('redirect_url', '')
            absurl = 'http://'+current_site + relativeLink
            # email_body = 'Hello, \n Use link below to reset your password  \n' + \
            #     absurl+"?redirect_url="+redirect_url
            email_body = 'Hello, \n Use link below to reset your password  \n' + \
                absurl
            data = {'email_body': email_body, 'to_email': user.user_email,
                    'email_subject': 'Reset your passsword'}
            Util.send_email(data)
        return Response({'success': 'We have sent you a link to reset your password'}, status=status.HTTP_200_OK)



class PasswordTokenCheckAPI(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def get(self, request, uidb64, token):

        try:
            id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(userid=id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({'error', 'Token is not valid, Please request a new link'}, status=status.HTTP_400_BAD_REQUEST)
            return Response({'success': True, 'message': 'Credentials valid', 'uidb64': uidb64, 'token': token }, status=status.HTTP_200_OK)

            
        except DjangoUnicodeDecodeError as identifier:
            # try:
            if not PasswordResetTokenGenerator().check_token(user):
                return Response({'error', 'Token is not valid, Please request a new link'}, status=status.HTTP_400_BAD_REQUEST)
                    
            
class SetNewPasswordAPIView(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'success': True, 'message': 'Password reset success'}, status=status.HTTP_200_OK)


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
            return User.objects.filter(user_email=user)



# class InAppChangePassword(generics.UpdateAPIView):
#     permission_classes = [permissions.IsAuthenticated]
#     serializer_class = InAppChangePasswordSerializer

#     def get_queryset(self):
#             user = self.request.user
#             print(User.objects.filter(Q(user_email=user) & Q())
#             return User.objects.filter(user_email=user)
    

class InAppChangePassword(generics.UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = InAppChangePasswordSerializer
    model = User

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            print('old password::::', self.object.check_password(serializer.data.get("old_password")))
            if not self.object.check_password(serializer.data.get("old_password")):
                
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

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

