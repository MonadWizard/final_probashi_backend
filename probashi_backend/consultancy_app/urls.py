from django.urls import path
from .views import ConsultancyCreateView, GetAllServicesPaginationView



urlpatterns = [
    path('consultancy-createview/', ConsultancyCreateView.as_view(), name="ConsultancyCreateView"),
    path('getall-services/', GetAllServicesPaginationView.as_view(), name="GetAllServicesPaginationView"),


]

