from django.urls import path
from .views import (
    GetAllUserPaginationView,
    GetSpecificUserView,
    FavouriteRequestSendView,
    FavouriteRequestsView,
    AcceptFavouriteRequest,
    RejectFavouriteRequest,
    FavouritesList,
    Friends_suggation,
    TakeMatchFriend,
    UserSearchGetData,
    UserSearchFilter,
    UserSearchField,
    unmatch_useres
)

# from user_connection_app import views

urlpatterns = [
    path("match-friend/", TakeMatchFriend.as_view(), name="match_friend"),
    path("user-search-field/", UserSearchField.as_view(), name="UserSearchField"),
    path(
        "user-search-filter-get/", UserSearchGetData.as_view(), name="UserSearchGetData"
    ),
    path("user-search-filter/", UserSearchFilter.as_view(), name="UserSearchFilter"),
    path(
        "userSearch/",
        GetAllUserPaginationView.as_view(),
        name="GetAllUserPaginationView",
    ),
    path(
        "specificuser/<str:user_id>/",
        GetSpecificUserView.as_view(),
        name="GetSpecificUserView",
    ),
    path(
        "favourite-request-send/",
        FavouriteRequestSendView.as_view(),
        name="FavouriteRequestSendView",
    ),
    path(
        "favourite-requests/",
        FavouriteRequestsView.as_view(),
        name="FavouriteRequestsView",
    ),
    path(
        "favourite-requests-accept/<str:requestid>/",
        AcceptFavouriteRequest.as_view(),
        name="AcceptFavouriteRequest",
    ),
    path(
        "favourite-requests-reject/<str:requestid>/",
        RejectFavouriteRequest.as_view(),
        name="RejectFavouriteRequest",
    ),
    path("favourite-list/", FavouritesList.as_view(), name="FavouritesList"),
    path("friend-suggation/", Friends_suggation.as_view(), name="Friends_suggation"),
    # now work with favourite request reject.
    path("unmatch-users/", unmatch_useres.as_view(), name="unmatch_useres"),

]
