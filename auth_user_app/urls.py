from django.urls import path
from .views import (
    MailVerifyRequestView,
    VerifyEmail,
    UpdateRegisterView,
    LogoutAPIView,
    SetNewPasswordAPIView,
    LoginAPIView,
    RequestPasswordResetEmail,
    VerifyForResetPasswordEmail,
    MailVerificationStatus,
    InAppChangePassword,
    RegistrationVerificationCodeSend,
    PhoneNumberRegistration,
    PhoneNumberLogin,
    LoginVerificationCodeSend,
    PhoneUpdateRegisterView,
    UserNameUniqueStatus,
    ChangeEmailVerifyAPIView,
    change_email_responseView,
    CheckChangableEmailView,
    DeleteUserView
)

from rest_framework_simplejwt.views import (
    TokenRefreshView,
)


urlpatterns = [
    path(
        "mail-verify-request/",
        MailVerifyRequestView.as_view(),
        name="mail-verify-request",
    ),
    path("email-verify/", VerifyEmail.as_view(), name="email-verify"),
    path(
        "emailverifstatus/", MailVerificationStatus.as_view(), name="emailverifystatus"
    ),
    path(
        "Update-register/<str:user_email>",
        UpdateRegisterView.as_view(),
        name="update-register",
    ),
    path("login/", LoginAPIView.as_view(), name="login"),
    path("logout/", LogoutAPIView.as_view(), name="auth_logout"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path(
        "request-reset-email/",
        RequestPasswordResetEmail.as_view(),
        name="request-reset-email",
    ),
    path(
        "verify-reset-email/",
        VerifyForResetPasswordEmail.as_view(),
        name="verify-reset-email",
    ),
    # path('password-reset/<uidb64>/<token>/',PasswordTokenCheckAPI.as_view(), name='password-reset-confirm'),
    path(
        "password-reset-complete/",
        SetNewPasswordAPIView.as_view(),
        name="password-reset-complete",
    ),
    path(
        "change-email-verify/",
        ChangeEmailVerifyAPIView.as_view(),
        name="ChangeEmailVerifyAPIView",
    ),
    path(
        "change-email-response/",
        change_email_responseView.as_view(),
        name="change-email-response",
    ),
    path(
        "check-changeable-email/",
        CheckChangableEmailView.as_view(),
        name="CheckChangableEmailView",
    ),
    path(
        "app/change-password/",
        InAppChangePassword.as_view(),
        name="InAppChangePassword",
    ),
    path(
        "phone-verification-otp/",
        RegistrationVerificationCodeSend.as_view(),
        name="VerificationCodeSend",
    ),
    path(
        "phone-number-registration/",
        PhoneNumberRegistration.as_view(),
        name="PhoneNumberRegistration",
    ),
    path(
        "phone-login-otp/",
        LoginVerificationCodeSend.as_view(),
        name="LoginVerificationCodeSend",
    ),
    path("phone-number-login/", PhoneNumberLogin.as_view(), name="PhoneNumberLogin"),
    path(
        "phone-update-register/<str:user_callphone>/",
        PhoneUpdateRegisterView.as_view(),
        name="PhoneUpdateRegisterView",
    ),
    path(
        "username-unique-status/",
        UserNameUniqueStatus.as_view(),
        name="UserNameUniqueStatus",
    ),

    path("delete-user/", DeleteUserView.as_view(), name="delete-user"),

]
