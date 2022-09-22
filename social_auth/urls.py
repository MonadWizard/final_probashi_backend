from django.urls import path

from .views import GoogleSocialAuthView, FacebookSocialAuthView, LinkedinSocialAuthView, AppleSocialAuthView

urlpatterns = [
    path("google/", GoogleSocialAuthView.as_view()),
    path("facebook/", FacebookSocialAuthView.as_view()),
    path("linkedin/", LinkedinSocialAuthView.as_view()),
    path("apple/", AppleSocialAuthView.as_view()),
    # path('social-complete-registration/', CompleteRegistrationSocialAuth.as_view()),
]
