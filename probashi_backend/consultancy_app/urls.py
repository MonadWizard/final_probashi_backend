from django.urls import path
from .views import (ConsultancyCreateView, 
                    GetAllServicesCategoryView,
                    AppointmentSeeker_ConsultantRequest, 
                    AppointmentSeeker_StarRating,
                    ConsultantProvider_StarRating,
                    AppointmentSeeker_MissingAppointmentReason,
                    GetServicesSpecificCategory)



urlpatterns = [
    path('consultancy-createview/', ConsultancyCreateView.as_view(), name="ConsultancyCreateView"),
    path('getall-services-category/', GetAllServicesCategoryView.as_view(), name="GetAllServicesPaginationView"),
    path('consultant-appointment-request/', AppointmentSeeker_ConsultantRequest.as_view(), name="AppointmentSeeker_ConsultantRequest"),
    path('appointment-seeker-star-rating/<str:id>/', AppointmentSeeker_StarRating.as_view(), name="AppointmentSeeker_StarRating"),
    path('consultant-provider-star-rating/<str:id>/', ConsultantProvider_StarRating.as_view(), name="ConsultantProvider_StarRating"),
    path('appointment-missing-reason/<str:id>/', AppointmentSeeker_MissingAppointmentReason.as_view(), name="AppointmentSeeker_MissingAppointmentReason"),
    path('services/<str:consultant_service_category>/', GetServicesSpecificCategory.as_view(), name="GetServicesSpecificCategory"),
    

]

