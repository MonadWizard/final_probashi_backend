from asyncio.log import logger
from cgitb import lookup
from dataclasses import field
from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField, Base64FileField
from .models import (ConsultancyCreate, UserConsultAppointmentRequest,
                    ConsultancyTimeSchudile, ConsultancyPayment)
from auth_user_app.models import User
import PyPDF2
import io
from user_connection_app.serializers import UserEducationSerializer, SerachUserSerializer





# class UserDataConsultancySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['user_industry', 'user_geolocation']

class ServiceCategorySerializer(serializers.ModelSerializer):
    # user_educationdata = UserEducationSerializer(many=True, read_only=True)
    # user_education = SerachUserSerializer(many=True, read_only=True)
    # user_data = UserDataConsultancySerializer(many=True, read_only=True)
    # user_educationdata = serializers.CharField(source="userid.user_fullname")

    class Meta:
        model = ConsultancyCreate
        # fields = [ 'id','userid', 'user_education', 'consultant_name']
        fields = ['consultant_service_category',]
        extra_kwargs = {'consultant_service_category': {"error_messages": {"required": "no service category"}}}



class GetServicesSpecificCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ConsultancyCreate
        # fields = [ 'id','userid', 'user_education', 'consultant_name']
        # fields = ['consultant_service_category',]
        fields = '__all__'
        extra_kwargs = {'__all__': {"error_messages": {"required": "field missing or incorrect"}}}
        





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
        extra_kwargs = {'__all__': {"error_messages": {"required": "field missing or incorrect"}}}





class ConsultancyTimeSchudileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConsultancyTimeSchudile
        fields = '__all__'
        extra_kwargs = {"--all__": {"error_messages": {"required": "field missing or incorrect"}}}


class GetAllServicesCategoryScheduleSerializer(serializers.ModelSerializer):
    consultancy_timeschudile = ConsultancyTimeSchudileSerializer(many=True, read_only=True)
    class Meta:
        model = ConsultancyCreate
        fields = ['id', 'consultant_name', 'consultant_service_category', 'consultancy_timeschudile' ]
        extra_kwargs = {'__all__': {"error_messages": {"required": "field missing or incorrect"}}}




# --------------------------------x-------------------------------x------------------

class FilteredListSerializer(serializers.ListSerializer):
    
    def to_representation(self, data):
        data = data.filter(is_consultancy_take=False)
        return super(FilteredListSerializer, self).to_representation(data)

class ConsultancyTimeSchudileNotTakenSerializer(serializers.ModelSerializer):

    class Meta:
        list_serializer_class = FilteredListSerializer
        model = ConsultancyTimeSchudile
        fields = '__all__'
        extra_kwargs = {"__all__": {"error_messages": {"required": "field missing or incorrect"}}}


class GetAllCategoryNotTakingScheduleSerializer(serializers.ModelSerializer):
    # consultancy_timeschudile = ConsultancyTimeSchudileNotTakenSerializer(many=True, read_only=True)
    consultancy_id = serializers.CharField(source='consultancyid.id')
    # consultancy_name = serializers.CharField(source='consultancyid.consultant_name')


    class Meta:
        model = ConsultancyTimeSchudile
        fields = '__all__'
        extra_kwargs = {"__all__": {"error_messages": {"required": "field missing or incorrect"}}}



# --------------------------------x-------------------------------x------------------




class ConsultantAppointmentRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserConsultAppointmentRequest
        # fields = '__all__'
        fields = ['seekerid',
                    'ConsultancyTimeSchudile','appointment_attendent_name',
                    'appointment_seeker_cellphone','appointment_seeker_email','appointment_seeker_note']
        extra_kwargs = {"__all__": {"error_messages": {"required": "field missing or incorrect"}}}



class AppointmentSeeker_StarRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserConsultAppointmentRequest
        fields = ['appointment_seeker_starrating', 'appointment_seeker_starrating_comment']
        extra_kwargs = {"__all__": {"error_messages": {"required": "field missing or incorrect"}}}


class ConsultantProvider_StarRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserConsultAppointmentRequest
        fields = ['consultant_provider_starratting', 'consultant_provider_starratting_comment']
        extra_kwargs = {"__all__": {"error_messages": {"required": "field missing or incorrect"}}}


class AppointmentSeeker_MissingAppointmentReasonSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserConsultAppointmentRequest
        fields = ['reason_for_missing_appointment']
        extra_kwargs = {"__all__": {"error_messages": {"required": "field missing or incorrect"}}}







class GetSpecificCategoryServiceSearchDataSerializer(serializers.ModelSerializer):
    user_id = serializers.CharField(source='userid.userid')

    class Meta:
        model = ConsultancyCreate
        fields = ['id', 'consultant_service_category','consultant_name', 'consultant_service_locationcountry', 'consultant_servicedescription','user_id']
        # fields = '__all__'
        extra_kwargs = {"__all__": {"error_messages": {"required": "field missing or incorrect"}}}



# ------------------------------------------------- pro user start------------------------------------------------------

# class BecomeProUserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
        # fields = ['is_pro_user']




# ------------------------------------------------- pro user end------------------------------------------------------

class ConsultancyPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConsultancyPayment
        fields = ['userid', 'consultancy_sheduleid', 'tran_id']
        extra_kwargs = {"__all__": {"error_messages": {"required": "field missing or incorrect"}}}
