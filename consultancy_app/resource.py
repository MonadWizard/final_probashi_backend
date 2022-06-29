from import_export import resources
from .models import (
    ConsultancyCreate,
    UserConsultAppointmentRequest,
    ConsultancyTimeSchudile,
    ProUserPayment,
    ConsultancyPayment,
)

class ConsultancyCreatePropertyAdminResource(resources.ModelResource):
    class Meta:
        model = ConsultancyCreate
        # exclude = ('id',)
        import_id_fields = ("userid",)


class UserConsultAppointmentRequestPropertyAdminResource(resources.ModelResource):
    class Meta:
        model = UserConsultAppointmentRequest
        import_id_fields = ('seekerid','ConsultancyTimeSchudile')


class ConsultancyTimeSchudilePropertyAdminResource(resources.ModelResource):
    class Meta:
        model = ConsultancyTimeSchudile
        # exclude = ('id',)
        import_id_fields = ("consultancyid",)


class ProUserPaymentPropertyAdminResource(resources.ModelResource):
    class Meta:
        model = ProUserPayment
        import_id_fields = ('userid',)


class ConsultancyPaymentPropertyAdminResource(resources.ModelResource):
    class Meta:
        model = ConsultancyPayment
        import_id_fields = ('userid','consultancy_sheduleid')

