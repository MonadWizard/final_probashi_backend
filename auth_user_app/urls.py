from django.urls import path
from .views import  (MailVerifyRequestView,
                    VerifyEmail,
                    UpdateRegisterView,
                    LogoutAPIView,
                    SetNewPasswordAPIView,
                    LoginAPIView,
                    RequestPasswordResetEmail,
                    ViewUser, 
                    MailVerificationStatus,
                    InAppChangePassword,
                    
                    RegistrationVerificationCodeSend,
                    PhoneNumberRegistration,
                    PhoneNumberLogin,
                    LoginVerificationCodeSend,
                    PhoneUpdateRegisterView,
                    
                    UserNameUniqueStatus)

from rest_framework_simplejwt.views import (
    TokenRefreshView,
)


urlpatterns = [
    path('mail-verify-request/', MailVerifyRequestView.as_view(), name='mail-verify-request'),
    path('email-verify/', VerifyEmail.as_view(), name="email-verify"),
    path('emailverifstatus/', MailVerificationStatus.as_view(), name="emailverifystatus"),
    path('Update-register/<str:user_email>', UpdateRegisterView.as_view(), name="update-register"),

    path('login/', LoginAPIView.as_view(), name="login"),
    path('logout/', LogoutAPIView.as_view(), name="auth_logout"),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('request-reset-email/', RequestPasswordResetEmail.as_view(),name="request-reset-email"),
    # path('password-reset/<uidb64>/<token>/',PasswordTokenCheckAPI.as_view(), name='password-reset-confirm'),
    path('password-reset-complete/', SetNewPasswordAPIView.as_view(),name='password-reset-complete'),
    path('userinfo/', ViewUser.as_view(), name="user-data"),
    path('app/change-password/', InAppChangePassword.as_view(), name='InAppChangePassword'),

    path('phone-verification-otp/', RegistrationVerificationCodeSend.as_view(), name='VerificationCodeSend'),
    path('phone-number-registration/', PhoneNumberRegistration.as_view(), name='PhoneNumberRegistration'),
    path('phone-login-otp/', LoginVerificationCodeSend.as_view(), name='LoginVerificationCodeSend'),
    path('phone-number-login/', PhoneNumberLogin.as_view(), name='PhoneNumberLogin'),
    path('phone-update-register/<str:user_callphone>/', PhoneUpdateRegisterView.as_view(), name='PhoneUpdateRegisterView'),

    path('username-unique-status/', UserNameUniqueStatus.as_view(), name='UserNameUniqueStatus'),

]
