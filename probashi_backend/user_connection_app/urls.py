from django.urls import path
from .views import (GetAllUserPaginationView, GetSpecificUserView, 
                    FavouriteRequestSendView, FavouriteRequestsView,
                    AcceptFavouriteRequest, RejectFavouriteRequest,
                    FavouritesList)



urlpatterns = [
    path('userSearch/', GetAllUserPaginationView.as_view(), name="GetAllUserPaginationView"),
    path('specificuser/<str:user_id>/', GetSpecificUserView.as_view(), name="GetSpecificUserView"),
    path('favourite-request-send/', FavouriteRequestSendView.as_view(), name="FavouriteRequestSendView"),
    path('favourite-requests/', FavouriteRequestsView.as_view(), name="FavouriteRequestsView"),
    path('favourite-requests-accept/<str:requestid>', AcceptFavouriteRequest.as_view(), name="AcceptFavouriteRequest"),
    path('favourite-requests-reject/<str:requestid>', RejectFavouriteRequest.as_view(), name="RejectFavouriteRequest"),
    path('favourite-list/', FavouritesList.as_view(), name="FavouritesList"),

    

    # now work with favourite request reject.

    
    

]

