from import_export import resources
from .models import UserFavoutireRequestSend, UserFavouriteList, FriendsSuggation


class UserFavoutireRequestSendPropertyAdminResource(resources.ModelResource):
    class Meta:
        model = UserFavoutireRequestSend
        # exclude = ('id',)
        import_id_fields = ("userid","favourite_request_to")


class UserFavouriteListPropertyAdminResource(resources.ModelResource):
    class Meta:
        model = UserFavouriteList
        import_id_fields = ("userid","favourite_userid",)


class FriendsSuggationPropertyAdminResource(resources.ModelResource):
    class Meta:
        model = FriendsSuggation
        # exclude = ('id',)
        import_id_fields = ("user",)

