from rest_framework import generics, status, views, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import permissions
from django.http import Http404
from .models import ConsultancyCreate
from .serializers import ConsultancyCreateSerializer



class ConsultancyCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = ConsultancyCreate.objects.all()
    serializer_class = ConsultancyCreateSerializer







