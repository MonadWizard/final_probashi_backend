from django.urls import path
from .views import (GetAllUserPaginationView, GetSpecificUserView, 
                    FavouriteRequestSendView, FavouriteRequestsView)



urlpatterns = [
    path('userSearch/', GetAllUserPaginationView.as_view(), name="GetAllUserPaginationView"),
    path('specificuser/<str:userid>', GetSpecificUserView.as_view(), name="GetSpecificUserView"),
    path('favourite-request-send/', FavouriteRequestSendView.as_view(), name="FavouriteRequestSendView"),
    path('favourite-requests/', FavouriteRequestsView.as_view(), name="FavouriteRequestsView"),

    
    

]

