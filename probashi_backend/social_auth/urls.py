from django.urls import path
# from .views import GoogleSocialAuthView, FacebookSocialAuthView, TwitterSocialAuthView
from .views import GoogleSocialAuthView

urlpatterns = [
    path('google/', GoogleSocialAuthView.as_view()),
    # path('facebook/', FacebookSocialAuthView.as_view()),


]
