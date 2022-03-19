from django.contrib import admin

# Register your models here.

from .models import ConsultancyCreate, UserConsultAppointmentRequest


admin.site.register(ConsultancyCreate)
admin.site.register(UserConsultAppointmentRequest)

