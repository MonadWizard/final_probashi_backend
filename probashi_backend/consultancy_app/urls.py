from django.urls import path
from .views import ConsultancyCreateView



urlpatterns = [
    path('consultancy-createview/', ConsultancyCreateView.as_view(), name="demo"),

]

