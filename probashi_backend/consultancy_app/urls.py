from django.urls import path
from .views import (ConsultancyCreateView, 
                    ConsultancyTimeSchudileView,
                    GetAllServicesCategorySchedule,
                    NotTakingScheduil_forEachService,

                    GetAllServicesCategoryView,
                    AppointmentSeeker_ConsultantRequest, 
                    AppointmentSeeker_StarRating,
                    ConsultantProvider_StarRating,
                    AppointmentSeeker_MissingAppointmentReason,
                    GetServicesSpecificCategoryData,

                    GetSpecificCategoryServiceSearchData,
                    BecomeProUser,
                    
                    ValidityWithIPN,

                    payment_success,
                    payment_fail,
                    payment_cancle)



urlpatterns = [
    path('consultancy-createview/', ConsultancyCreateView.as_view(), name="ConsultancyCreateView"),
    path('consultancy-schudile/', ConsultancyTimeSchudileView.as_view(), name="ConsultancyTimeSchudileView"),
    path('services-category-schedule/', GetAllServicesCategorySchedule.as_view(), name="GetAllServicesCategorySchedule"), #

    path('getall-services-category/', GetAllServicesCategoryView.as_view(), name="GetAllServicesPaginationView"),
    path('specific-service-searchdata/<str:service_Category>/', GetSpecificCategoryServiceSearchData.as_view(), name="GetSpecificCategoryServiceSearchData"),

    path('nottaking-scheduile/<str:service_Category>/', NotTakingScheduil_forEachService.as_view(), name="NotTakingScheduil_forEachService"),
    path('consultant-appointment-request/', AppointmentSeeker_ConsultantRequest.as_view(), name="AppointmentSeeker_ConsultantRequest"),
    
    path('appointment-seeker-star-rating/<str:id>/', AppointmentSeeker_StarRating.as_view(), name="AppointmentSeeker_StarRating"),
    path('consultant-provider-star-rating/<str:id>/', ConsultantProvider_StarRating.as_view(), name="ConsultantProvider_StarRating"),
    path('appointment-missing-reason/<str:id>/', AppointmentSeeker_MissingAppointmentReason.as_view(), name="AppointmentSeeker_MissingAppointmentReason"),
    
    path('pro/', BecomeProUser.as_view(), name="BecomeProUser"),
    
    #not used
    path('services/<str:consultant_service_category>/', GetServicesSpecificCategoryData.as_view(), name="GetServicesSpecificCategoryData"),

    # payment
    path('validity/', ValidityWithIPN.as_view(), name="payment_success"),

    # success fail cancle redirect URL
    path('success/', payment_success, name="payment_success"),
    path('fail/', payment_fail, name="payment_fail"),
    path('cancle/', payment_cancle, name="payment_cancle"),
]

