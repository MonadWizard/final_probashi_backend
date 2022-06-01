from django.urls import path
from .views import (
    ConsultancyCreateView,
    ConsultancyTimeSchudileView,
    GetAllServicesCategorySchedule,
    NotTakingScheduil_forSpecificUser,
    ALLScheduils_forConsultancyProvider,
    GetAllServicesCategoryView,
    AppointmentSeeker_ConsultantRequest,
    AppointmentSeeker_StarRating,
    ConsultantProvider_StarRating,
    AppointmentSeeker_MissingAppointmentReason,
    SpecificServicesSchedules,
    GetSpecificCategoryServiceSearchData,
    BecomeProUser,
    Pro_Payment_success,
    Pro_Payment_fail,
    Pro_Payment_cancle,
    Consultancy_Payment_success,
    Consultancy_Payment_fail,
    Consultancy_Payment_cancle,
    ServiceSearchGetData,
    ServiceSearchFilter,
    ServiceSearchField,
    SpecificServiceDescription,
    ConsultancyInfo,
    IpnSslcommerze,
)


urlpatterns = [
    path(
        "consultancy-createview/",
        ConsultancyCreateView.as_view(),
        name="ConsultancyCreateView",
    ),
    path(
        "consultancy-schudile/",
        ConsultancyTimeSchudileView.as_view(),
        name="ConsultancyTimeSchudileView",
    ),
    path(
        "services-category-schedule/",
        GetAllServicesCategorySchedule.as_view(),
        name="GetAllServicesCategorySchedule",
    ),  #
    path(
        "specific-service/",
        SpecificServicesSchedules.as_view(),
        name="SpecificServicesSchedules",
    ),
    path(
        "all-schedule/",
        ALLScheduils_forConsultancyProvider.as_view(),
        name="ALLScheduils_forConsultancyProvider",
    ),
    path(
        "getall-services-category/",
        GetAllServicesCategoryView.as_view(),
        name="GetAllServicesPaginationView",
    ),
    path(
        "specific-service-searchdata/<str:service_Category>/",
        GetSpecificCategoryServiceSearchData.as_view(),
        name="GetSpecificCategoryServiceSearchData",
    ),
    path(
        "nottaking-scheduile/",
        NotTakingScheduil_forSpecificUser.as_view(),
        name="NotTakingScheduil_forEachService",
    ),
    path(
        "consultant-appointment-request/",
        AppointmentSeeker_ConsultantRequest.as_view(),
        name="AppointmentSeeker_ConsultantRequest",
    ),
    path(
        "appointment-seeker-star-rating/<str:ConsultancyTimeSchudile>/",
        AppointmentSeeker_StarRating.as_view(),
        name="AppointmentSeeker_StarRating",
    ),
    path(
        "consultant-provider-star-rating/<str:ConsultancyTimeSchudile>/",
        ConsultantProvider_StarRating.as_view(),
        name="ConsultantProvider_StarRating",
    ),
    path(
        "appointment-missing-reason/<str:ConsultancyTimeSchudile>/",
        AppointmentSeeker_MissingAppointmentReason.as_view(),
        name="AppointmentSeeker_MissingAppointmentReason",
    ),
    path("pro/", BecomeProUser.as_view(), name="BecomeProUser"),
    # payment
    path("pro-success/", Pro_Payment_success.as_view(), name="payment_success"),
    path("pro-fail/", Pro_Payment_fail, name="payment_fail"),
    path("pro-cancle/", Pro_Payment_cancle, name="payment_cancle"),
    # consultancy success fail cancle redirect URL
    path("ipn/", IpnSslcommerze.as_view()),
    path(
        "consultancy-success/",
        Consultancy_Payment_success.as_view(),
        name="payment_success",
    ),
    path("consultancy-fail/", Consultancy_Payment_fail, name="payment_fail"),
    path("consultancy-cancle/", Consultancy_Payment_cancle, name="payment_cancle"),
    path(
        "service-search-data/",
        ServiceSearchGetData.as_view(),
        name="ServiceSearchGetData",
    ),
    path(
        "service-search-filter/",
        ServiceSearchFilter.as_view(),
        name="ServiceSearchFilter",
    ),
    path(
        "service-search-field/", ServiceSearchField.as_view(), name="ServiceSearchField"
    ),
    path(
        "service-description/<str:service_id>/",
        SpecificServiceDescription.as_view(),
        name="SpecificServiceDescription",
    ),
    path("consultancy-info/", ConsultancyInfo.as_view(), name="ConsultancyInfo"),
]
