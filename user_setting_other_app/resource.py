from import_export import resources
from .models import PromoCodeData, StaticSettingData


class PromoCodeDataPropertyAdminResource(resources.ModelResource):
    class Meta:
        model = PromoCodeData
        # exclude = ('id',)
        import_id_fields = ("promo_code",)


class StaticSettingDataPropertyAdminResource(resources.ModelResource):
    class Meta:
        model = StaticSettingData
        # import_id_fields = ('id',)
