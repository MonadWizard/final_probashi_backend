from django.urls import path
from .views import (UserProfileSkipPart1, UserProfileSkipPart2,
                    UserEditProfile, UserAboutSocialLinkCreate, 
                    UserAboutSocialLinkUpdate, UserExperienceCreate, 
                    UserExperienceUpdate)



urlpatterns = [
    path('user-profile-skip1/<str:userid>/', UserProfileSkipPart1.as_view(), name="UserProfileskip1"),
    path('user-profile-skip2/<str:userid>/', UserProfileSkipPart2.as_view(), name="UserProfileskip2"),
    path('user-edit-profile/<str:userid>/', UserEditProfile.as_view(), name="UserEditProfile"),
    path('user-about-social-link-create/', UserAboutSocialLinkCreate.as_view(), name="UserAboutSocialLinkCreate"),
    path('user-about-social-link-update/<str:userid>/', UserAboutSocialLinkUpdate.as_view(), name="UserAboutSocialLinkUpdate"),
    path('user-experience-create/', UserExperienceCreate.as_view(), name="UserExperienceCreate"),
    path('user-experience-update/<str:userid>/', UserExperienceUpdate.as_view(), name="UserExperienceUpdate"),


]

