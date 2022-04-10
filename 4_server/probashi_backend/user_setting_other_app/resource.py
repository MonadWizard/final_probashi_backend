from import_export import resources
from .models import PromoCodeData

class PropertyAdminResource(resources.ModelResource):
    class Meta:
        model = PromoCodeData
        # exclude = ('id',)
        import_id_fields = ('promo_code',)