from rest_framework import generics, status, views, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import permissions
from django.http import Http404
from .models import ConsultancyCreate
from .serializers import (ConsultancyCreateSerializer, SearchServiceSerializer)
from rest_framework.pagination import PageNumberPagination



class ConsultancyCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = ConsultancyCreate.objects.all()
    serializer_class = ConsultancyCreateSerializer



class GetAllServiceSetPagination(PageNumberPagination):
    page_size = 2
    page_size_query_param = 'services'
    max_page_size = 10000

class GetAllServicesPaginationView(generics.ListAPIView):
    queryset = ConsultancyCreate.objects.all()
    serializer_class = SearchServiceSerializer
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = GetAllServiceSetPagination





