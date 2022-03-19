from asyncio.log import logger
from dataclasses import field
from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField, Base64FileField
from .models import (ConsultancyCreate, UserConsultAppointmentRequest)
from auth_user_app.models import User
import PyPDF2
import io
from user_connection_app.serializers import UserEducationSerializer, SerachUserSerializer





class UserDataConsultancySerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_industry', 'user_geolocation']

class SearchServiceSerializer(serializers.ModelSerializer):
    # user_educationdata = UserEducationSerializer(many=True, read_only=True)
    user_education = SerachUserSerializer(many=True, read_only=True)
    # user_data = UserDataConsultancySerializer(many=True, read_only=True)
    # user_educationdata = serializers.CharField(source="userid.user_fullname")

    class Meta:
        model = ConsultancyCreate
        fields = [ 'id','userid', 'user_education', 'consultant_name']
        # fields = '__all__'






class PDFBase64File(Base64FileField):
    ALLOWED_TYPES = ['pdf']

    def get_file_extension(self, filename, decoded_file):
        try:
            PyPDF2.PdfFileReader(io.BytesIO(decoded_file))
        except PyPDF2.utils.PdfReadError as e:
            logger.warning(e)
        else:
            return 'pdf'

class ConsultancyCreateSerializer(serializers.ModelSerializer):
    consultant_servicedetail_filepath=PDFBase64File() # From DRF Extra Fields
    consultant_cvpath = PDFBase64File()
    consultant_idverification_passportimagepath = Base64ImageField()
    class Meta:
        model = ConsultancyCreate
        fields = '__all__'



class ConsultantAppointmentRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserConsultAppointmentRequest
        # fields = '__all__'
        exclude = ['appointment_seeker_starrating','appointment_seeker_starrating_comment',
                    'consultant_provider_starratting','consultant_provider_starratting_comment',
                    'reason_for_missing_appointment']
        

class AppointmentSeeker_StarRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserConsultAppointmentRequest
        fields = ['appointment_seeker_starrating', 'appointment_seeker_starrating_comment']


class ConsultantProvider_StarRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserConsultAppointmentRequest
        fields = ['consultant_provider_starratting', 'consultant_provider_starratting_comment']


class AppointmentSeeker_MissingAppointmentReasonSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserConsultAppointmentRequest
        fields = ['reason_for_missing_appointment']








