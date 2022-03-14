from django.urls import path
from .views import (UserIndustryDataView, UserAreaOfExperienceDataView,
                    UserInterestedAreaDataView, UserGoalDataView,
                    ConsultancyServiceCategoryDataView,
                    CreateOtherRowsInStaticTableView)



urlpatterns = [
    path('UserIndustryData/', UserIndustryDataView.as_view(), name="UserIndustryDataView"),
    path('UserAreaOfExperienceData/', UserAreaOfExperienceDataView.as_view(), name="UserAreaOfExperienceDataView"),
    path('UserInterestedAreaData/', UserInterestedAreaDataView.as_view(), name="UserInterestedAreaDataView"),
    path('UserGoalData/', UserGoalDataView.as_view(), name="UserGoalDataView"),
    path('ConsultancyServiceCategoryData/', ConsultancyServiceCategoryDataView.as_view(), name="ConsultancyServiceCategoryDataView"),
    path('other-rows/', CreateOtherRowsInStaticTableView.as_view(), name="CreateOtherRowsInStaticTableView"),




]

