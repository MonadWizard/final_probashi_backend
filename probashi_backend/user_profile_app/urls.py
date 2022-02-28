from django.urls import path
from .views import DemoView, UserProfile



urlpatterns = [
    path('demo/', DemoView.as_view(), name="demo"),
    path('UserProfile/', UserProfile.as_view(), name="UserProfile")

]

