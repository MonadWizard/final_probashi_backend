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
                    Pro_Payment_success,
                    Pro_Payment_fail,
                    Pro_Payment_cancle,
                    Consultancy_Payment_success,
                    Consultancy_Payment_fail,
                    Consultancy_Payment_cancle)



urlpatterns = [
    path('consultancy-createview/', ConsultancyCreateView.as_view(), name="ConsultancyCreateView"),
    path('consultancy-schudile/', ConsultancyTimeSchudileView.as_view(), name="ConsultancyTimeSchudileView"),
    path('services-category-schedule/', GetAllServicesCategorySchedule.as_view(), name="GetAllServicesCategorySchedule"), #

    path('getall-services-category/', GetAllServicesCategoryView.as_view(), name="GetAllServicesPaginationView"),
    path('specific-service-searchdata/<str:service_Category>/', GetSpecificCategoryServiceSearchData.as_view(), name="GetSpecificCategoryServiceSearchData"),

    path('nottaking-scheduile/', NotTakingScheduil_forEachService.as_view(), name="NotTakingScheduil_forEachService"),
    path('consultant-appointment-request/', AppointmentSeeker_ConsultantRequest.as_view(), name="AppointmentSeeker_ConsultantRequest"),
    
    path('appointment-seeker-star-rating/<str:id>/', AppointmentSeeker_StarRating.as_view(), name="AppointmentSeeker_StarRating"),
    path('consultant-provider-star-rating/<str:id>/', ConsultantProvider_StarRating.as_view(), name="ConsultantProvider_StarRating"),
    path('appointment-missing-reason/<str:id>/', AppointmentSeeker_MissingAppointmentReason.as_view(), name="AppointmentSeeker_MissingAppointmentReason"),
    
    path('pro/', BecomeProUser.as_view(), name="BecomeProUser"),
    
    #not used
    path('services/<str:consultant_service_category>/', GetServicesSpecificCategoryData.as_view(), name="GetServicesSpecificCategoryData"),

    # payment
    # path('validity/', ValidityWithIPN.as_view(), name="payment_success"),

    # pro user success fail cancle redirect URL
    path('pro-success/', Pro_Payment_success.as_view(), name="payment_success"),
    path('pro-fail/', Pro_Payment_fail, name="payment_fail"),
    path('pro-cancle/', Pro_Payment_cancle, name="payment_cancle"),

    # consultancy success fail cancle redirect URL
    path('consultancy-success/', Consultancy_Payment_success.as_view(), name="payment_success"),
    path('consultancy-fail/', Consultancy_Payment_fail, name="payment_fail"),
    path('consultancy-cancle/', Consultancy_Payment_cancle, name="payment_cancle"),



]

