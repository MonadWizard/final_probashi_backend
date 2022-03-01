from django.urls import path
from .views import UserProfileSkipPart1, UserProfileSkipPart2, UserAboutSocialLink



urlpatterns = [
    path('user-profile-skip1/<str:userid>/', UserProfileSkipPart1.as_view(), name="UserProfileskip1"),
    path('user-profile-skip2/<str:userid>/', UserProfileSkipPart2.as_view(), name="UserProfileskip2"),
    path('user-about-social-link/<str:userid>/', UserAboutSocialLink.as_view(), name="UserAboutSocialLink"),

]

