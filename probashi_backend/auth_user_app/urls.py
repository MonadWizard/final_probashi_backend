from django.urls import path
from .views import  (MailVerifyRequestView,
                    VerifyEmail,
                    UpdateRegisterView,
                    LogoutAPIView,
                    SetNewPasswordAPIView,
                    LoginAPIView,
                    PasswordTokenCheckAPI,
                    RequestPasswordResetEmail,
                    ViewUser)
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)


urlpatterns = [
    path('mail-verify-request/', MailVerifyRequestView.as_view(), name='mail-verify-request'),
    path('email-verify/', VerifyEmail.as_view(), name="email-verify"),
    path('Update-register/<str:user_email>', UpdateRegisterView.as_view(), name="update-register"),

    path('login/', LoginAPIView.as_view(), name="login"),
    path('logout/', LogoutAPIView.as_view(), name="logout"),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('request-reset-email/', RequestPasswordResetEmail.as_view(),name="request-reset-email"),
    path('password-reset/<uidb64>/<token>/',PasswordTokenCheckAPI.as_view(), name='password-reset-confirm'),
    path('password-reset-complete/', SetNewPasswordAPIView.as_view(),name='password-reset-complete'),
    path('userinfo/', ViewUser.as_view(), name="user-data"),
]
