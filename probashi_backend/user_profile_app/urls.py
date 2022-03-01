from django.urls import path
from .views import UserProfileSkipPart1, UserProfileSkipPart2



urlpatterns = [
    path('user-profile-skip1/<str:userid>/', UserProfileSkipPart1.as_view(), name="UserProfileskip1"),
    path('user-profile-skip2/<str:userid>/', UserProfileSkipPart2.as_view(), name="UserProfileskip2")

]

