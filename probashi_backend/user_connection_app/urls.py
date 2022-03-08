from django.urls import path
from .views import GetAllUserPaginationView



urlpatterns = [
    path('userSearch/', GetAllUserPaginationView.as_view(), name="search_user_list"),

]

