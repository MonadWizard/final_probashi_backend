from django.urls import path
from .views import (GetAllUserPaginationView, GetSpecificUserView, ConnectionRequestSendView)



urlpatterns = [
    path('userSearch/', GetAllUserPaginationView.as_view(), name="search_user_list"),
    path('specificuser/<str:userid>', GetSpecificUserView.as_view(), name="search_user_list"),
    path('connection-request/', ConnectionRequestSendView.as_view(), name="search_user_list"),

    
    

]

