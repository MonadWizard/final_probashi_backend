from django.urls import path
from .views import BlogCreateView



urlpatterns = [
    path('blog-create/', BlogCreateView.as_view(), name="BlogCreateView"),

]

