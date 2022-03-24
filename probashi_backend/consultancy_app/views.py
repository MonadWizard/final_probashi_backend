from cgitb import lookup
from urllib import request
from rest_framework import generics, status, views, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import permissions
from django.http import Http404
from .models import (ConsultancyCreate, UserConsultAppointmentRequest)
from .serializers import (ConsultancyCreateSerializer, SearchServiceSerializer,
                        ConsultantAppointmentRequestSerializer, AppointmentSeeker_StarRatingSerializer,
                        ConsultantProvider_StarRatingSerializer, AppointmentSeeker_MissingAppointmentReasonSerializer)
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
from auth_user_app.models import User



class GetAllServiceSetPagination(PageNumberPagination):
    page_size = 20
    # page_size_query_param = 'services'
    max_page_size = 10000

class GetAllServicesPaginationView(generics.ListAPIView):
    queryset = ConsultancyCreate.objects.all()
    serializer_class = SearchServiceSerializer
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = GetAllServiceSetPagination



class ConsultancyCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = ConsultancyCreate.objects.all()
    serializer_class = ConsultancyCreateSerializer


class AppointmentSeeker_ConsultantRequest(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = UserConsultAppointmentRequest.objects.all()
    serializer_class = ConsultantAppointmentRequestSerializer

    def create(self, request, *args, **kwargs):
        serializer = ConsultantAppointmentRequestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AppointmentSeeker_StarRating(generics.UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    # queryset = UserConsultAppointmentRequest.objects.all()
    serializer_class = AppointmentSeeker_StarRatingSerializer
    lookup_field = 'id'

    def get_queryset(self):
        try:
            user = self.request.user
            # user_id = User.objects.filter(user_email=user).values('userid')
            # user_id = user_id[0].get('userid')
            # print('id::::::::::::', self.kwargs.get('id'))
            return UserConsultAppointmentRequest.objects.filter(seekerid=user)
        except UserConsultAppointmentRequest.DoesNotExist:
            raise Http404


class ConsultantProvider_StarRating(generics.UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ConsultantProvider_StarRatingSerializer
    lookup_field = 'id'

    def get_queryset(self):
        try:
            user = self.request.user
            return UserConsultAppointmentRequest.objects.filter(consultantid__userid=user)
        except UserConsultAppointmentRequest.DoesNotExist:
            raise Http404




class AppointmentSeeker_MissingAppointmentReason(generics.UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = AppointmentSeeker_MissingAppointmentReasonSerializer
    lookup_field = 'id'

    def get_queryset(self):
        try:
            user = self.request.user
            return UserConsultAppointmentRequest.objects.filter(seekerid=user)
        except UserConsultAppointmentRequest.DoesNotExist:
            raise Http404






