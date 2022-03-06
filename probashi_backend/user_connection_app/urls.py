from django.urls import path
from .views import SearchUserList



urlpatterns = [
    path('userSearch/', SearchUserList.as_view(), name="search_user_list"),

]

