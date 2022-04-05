from django.urls import path
from .views import CreateFriendsMathcTable



urlpatterns = [
    path('create-friend-match-table/', CreateFriendsMathcTable, name="CreateFriendsMathcTable"),

]

