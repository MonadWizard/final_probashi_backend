from django.urls import path
from .views import (
    UserIndustryDataView,
    UserAreaOfExperienceDataView,
    UserInterestedAreaDataView,
    UserGoalDataView,
    ConsultancyServiceCategoryDataView,
    CreateOtherRowsInStaticTableView,
    BlogTagDataView,
    UserEducationDataView,
    FatchingTrubleView,
    FaqView,
    privacypolicyView,
    NotificationView,
    updateNotificationStatusView,
    DeleteNotificationView,
    UserSettingsOptionView,
    EducationServiceDataView,
    OverseasRecruitmentServiceDataView,
    MedicalConsultancyServiceDataView,
    LegalCivilServiceDataView,
    PropertyManagementServiceDataView,
    TourismServiceDataView,
    TrainingServiceDataView,
    DigitalServiceDataView,
    TradeFacilitationServiceDataView,
    SpecificConsultancyData,
    GetCityView,
    UserCurrentDesignationDataView,
    region_country
)


urlpatterns = [
    path(
        "UserIndustryData/", UserIndustryDataView.as_view(), name="UserIndustryDataView"
    ),
    path(
        "UserAreaOfExperienceData/",
        UserAreaOfExperienceDataView.as_view(),
        name="UserAreaOfExperienceDataView",
    ),
    path(
        "UserCurrentDesignationData/",
        UserCurrentDesignationDataView.as_view(),
        name="UserCurrentDesignationDataView",
    ),
    path(
        "UserInterestedAreaData/",
        UserInterestedAreaDataView.as_view(),
        name="UserInterestedAreaDataView",
    ),
    path("UserGoalData/", UserGoalDataView.as_view(), name="UserGoalDataView"),
    path(
        "ConsultancyServiceCategoryData/",
        ConsultancyServiceCategoryDataView.as_view(),
        name="ConsultancyServiceCategoryDataView",
    ),
    path(
        "other-rows/",
        CreateOtherRowsInStaticTableView.as_view(),
        name="CreateOtherRowsInStaticTableView",
    ),
    path("blog-tagData/", BlogTagDataView.as_view(), name="BlogTagDataView"),
    path(
        "user-educationData/",
        UserEducationDataView.as_view(),
        name="UserEducationDataView",
    ),
    path(
        "user-fatching-truble/", FatchingTrubleView.as_view(), name="FatchingTrubleView"
    ),
    path("faq/", FaqView.as_view(), name="FaqView"),
    path("privacy-pilicy/", privacypolicyView.as_view(), name="privacypolicyView"),
    path("notification/", NotificationView.as_view(), name="NotificationView"),
    path(
        "update-notification/<str:notificationid>/",
        updateNotificationStatusView.as_view(),
        name="updateNotificationStatusView",
    ),
    path(
        "delete-notification/<str:notificationid>/",
        DeleteNotificationView.as_view(),
        name="DeleteNotificationView",
    ),
    path(
        "user-setting/<str:userid>/",
        UserSettingsOptionView.as_view(),
        name="UserSettingsOptionView",
    ),
    path(
        "consultancy-category-data/",
        SpecificConsultancyData.as_view(),
        name="SpecificConsultancyData",
    ),
    path(
        "education-service-data/",
        EducationServiceDataView.as_view(),
        name="EducationServiceDataView",
    ),
    path(
        "overseas-recruitment-service-data/",
        OverseasRecruitmentServiceDataView.as_view(),
        name="OverseasRecruitmentServiceDataView",
    ),
    path(
        "medical-consultancy-service-data/",
        MedicalConsultancyServiceDataView.as_view(),
        name="MedicalConsultancyServiceDataView",
    ),
    path(
        "legal-civil-service-data/",
        LegalCivilServiceDataView.as_view(),
        name="LegalCivilServiceDataView",
    ),
    path(
        "property-management-service-data/",
        PropertyManagementServiceDataView.as_view(),
        name="PropertyManagementServiceDataView",
    ),
    path(
        "tourism-service-data/",
        TourismServiceDataView.as_view(),
        name="TourismServiceDataView",
    ),
    path(
        "training-service-data/",
        TrainingServiceDataView.as_view(),
        name="TrainingServiceDataView",
    ),
    path(
        "digital-service-data/",
        DigitalServiceDataView.as_view(),
        name="DigitalServiceDataView",
    ),
    path(
        "trade-facilitation-service-data/",
        TradeFacilitationServiceDataView.as_view(),
        name="TradeFacilitationServiceDataView",
    ),
    path("city-get/", GetCityView.as_view(), name="city-get"),

    path("region-country/", region_country.as_view(), name="region_country"),
]
