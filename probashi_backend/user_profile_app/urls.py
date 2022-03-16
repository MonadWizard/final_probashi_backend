from django.urls import path
from .views import (UserProfileSkipPart1, UserProfileSkipPart2,
                    UserEditProfile, UserAboutSocialLinkUpdate, 
                    UserExperienceCreate, UserEducationCreate,
                    UserIdVerificationCreate,UserProfileView,
                    UserInterestedAreaView, UserGoalView,UserExperienceUpdate
                    )



urlpatterns = [
    path('user-profile-skip1/<str:userid>/', UserProfileSkipPart1.as_view(), name="UserProfileskip1"),
    path('user-profile-skip2/<str:userid>/', UserProfileSkipPart2.as_view(), name="UserProfileskip2"),
    path('user-edit-profile/<str:userid>/', UserEditProfile.as_view(), name="UserEditProfile"),
    path('user-about-social-link-update/<str:userid>/', UserAboutSocialLinkUpdate.as_view(), name="UserAboutSocialLinkUpdate"),
    path('user-experience-create/', UserExperienceCreate.as_view(), name="UserExperienceCreate"),
    path('user-experience-update/<str:userid>/', UserExperienceUpdate.as_view(), name="UserExperienceUpdate"),
    path('user-education-create/', UserEducationCreate.as_view(), name="UserEducationCreate"),
    path('user-idverify-create/', UserIdVerificationCreate.as_view(), name="UserIdVerificationCreate"),
    path('user-profile-view/', UserProfileView.as_view(), name="UserProfileView"),
    path('user-interestedareas/<str:userid>/', UserInterestedAreaView.as_view(), name="UserInterestedAreaView"),
    path('user-goals/<str:userid>/', UserGoalView.as_view(), name="UserGoalView"),


    
]

