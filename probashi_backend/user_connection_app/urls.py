from django.urls import path
from .views import (GetAllUserPaginationView, GetSpecificUserView, FavouriteRequestSendView)



urlpatterns = [
    path('userSearch/', GetAllUserPaginationView.as_view(), name="search_user_list"),
    path('specificuser/<str:userid>', GetSpecificUserView.as_view(), name="search_user_list"),
    path('favourite-request-send/', FavouriteRequestSendView.as_view(), name="search_user_list"),

    
    

]

