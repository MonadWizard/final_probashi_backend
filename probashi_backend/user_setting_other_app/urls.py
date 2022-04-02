from django.urls import path
from .views import (UserIndustryDataView, UserAreaOfExperienceDataView,
                    UserInterestedAreaDataView, UserGoalDataView,
                    ConsultancyServiceCategoryDataView,
                    CreateOtherRowsInStaticTableView, BlogTagDataView,
                    UserEducationDataView,
                    FatchingTrubleView, 
                    FaqView,privacypolicyView,NotificationView)



urlpatterns = [
    path('UserIndustryData/', UserIndustryDataView.as_view(), name="UserIndustryDataView"),
    path('UserAreaOfExperienceData/', UserAreaOfExperienceDataView.as_view(), name="UserAreaOfExperienceDataView"),
    path('UserInterestedAreaData/', UserInterestedAreaDataView.as_view(), name="UserInterestedAreaDataView"),
    path('UserGoalData/', UserGoalDataView.as_view(), name="UserGoalDataView"),
    path('ConsultancyServiceCategoryData/', ConsultancyServiceCategoryDataView.as_view(), name="ConsultancyServiceCategoryDataView"),
    path('other-rows/', CreateOtherRowsInStaticTableView.as_view(), name="CreateOtherRowsInStaticTableView"),
    path('blog-tagData/', BlogTagDataView.as_view(), name="BlogTagDataView"),
    path('user-educationData/', UserEducationDataView.as_view(), name="UserEducationDataView"),
    path('user-fatching-truble/', FatchingTrubleView.as_view(), name="FatchingTrubleView"),
    path('faq/', FaqView.as_view(), name="FaqView"),
    path('privacy-pilicy/', privacypolicyView.as_view(), name="privacypolicyView"),
    path('notification/', NotificationView.as_view(), name="NotificationView"),
    



]

