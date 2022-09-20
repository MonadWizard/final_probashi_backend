from import_export import resources
from .models import (
    StaticSettingData,
    PromoCodeData,
    User_settings,
    Notification,
    Facing_trouble,
)

class PromoCodeDataPropertyAdminResource(resources.ModelResource):
    class Meta:
        model = PromoCodeData
        # exclude = ('id',)
        import_id_fields = ("promo_code",)


class StaticSettingDataPropertyAdminResource(resources.ModelResource):
    class Meta:
        model = StaticSettingData
        # import_id_fields = ('id',)


class User_settingsPropertyAdminResource(resources.ModelResource):
    class Meta:
        model = User_settings
        # exclude = ('id',)
        import_id_fields = ("userid",)


class NotificationPropertyAdminResource(resources.ModelResource):
    class Meta:
        model = Notification
        # exclude = ('id',)
        import_id_fields = ("userid","receiverid")


class Facing_troublePropertyAdminResource(resources.ModelResource):
    class Meta:
        model = Facing_trouble
        # exclude = ('id',)
        import_id_fields = ("user",)
