from asyncio.log import logger
from cgitb import lookup
from dataclasses import field
from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField, Base64FileField
from .models import (
    ConsultancyCreate,
    UserConsultAppointmentRequest,
    ConsultancyTimeSchudile,
    ConsultancyPayment,
)
from auth_user_app.models import User
import PyPDF2
import io


class ServiceCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = ConsultancyCreate
        fields = [
            "consultant_service_category",
        ]



class PDFBase64File(Base64FileField):
    ALLOWED_TYPES = ["pdf"]

    def get_file_extension(self, filename, decoded_file):
        try:
            PyPDF2.PdfFileReader(io.BytesIO(decoded_file))
        except PyPDF2.utils.PdfReadError as e:
            logger.warning(e)
        else:
            return "pdf"


class ConsultancyCreateSerializer(serializers.ModelSerializer):
    consultant_servicedetail_filepath = PDFBase64File()  # From DRF Extra Fields
    consultant_cvpath = PDFBase64File()
    consultant_idverification_passportimagepath = Base64ImageField()

    class Meta:
        model = ConsultancyCreate
        fields = "__all__"


class ConsultancyTimeSchudileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConsultancyTimeSchudile
        fields = "__all__"


class GetAllCategoryScheduleSerializer(serializers.ModelSerializer):
    consultancy_timeschudiles = ConsultancyTimeSchudileSerializer(
        source="consultancy_timeschudile", many=True, read_only=True
    )

    class Meta:
        model = ConsultancyCreate
        fields = [
            "id",
            "consultant_name",
            "consultant_service_category",
            "consultancy_timeschudiles",
        ]


class FilteredListSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        data = data.filter(is_consultancy_take=False)
        return super(FilteredListSerializer, self).to_representation(data)


class ConsultancyTimeSchudileNotTakenSerializer(serializers.ModelSerializer):
    class Meta:
        list_serializer_class = FilteredListSerializer
        model = ConsultancyTimeSchudile
        fields = "__all__"


class GetAllCategoryNotTakingScheduleSerializer(serializers.ModelSerializer):
    consultancy_timeschudiles = ConsultancyTimeSchudileNotTakenSerializer(
        source="consultancy_timeschudile", many=True, read_only=True
    )

    class Meta:
        model = ConsultancyCreate
        fields = [
            "id",
            "consultant_name",
            "consultant_service_category",
            "consultancy_timeschudiles",
        ]


class GetAllServicesCategoryScheduleSerializer(serializers.ModelSerializer):
    consultancy_timeschudile = ConsultancyTimeSchudileNotTakenSerializer(
        many=True, read_only=True
    )

    class Meta:
        model = ConsultancyCreate
        fields = [
            "id",
            "consultant_name",
            "consultant_service_category",
            "consultancy_timeschudile",
        ]



class ConsultantAppointmentRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserConsultAppointmentRequest
        fields = [
            "seekerid",
            "ConsultancyTimeSchudile",
            "appointment_attendent_name",
            "appointment_seeker_cellphone",
            "appointment_seeker_email",
            "appointment_seeker_note",
        ]


class AppointmentSeeker_StarRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserConsultAppointmentRequest
        fields = [
            "appointment_seeker_starrating",
            "appointment_seeker_starrating_comment",
        ]


class ConsultantProvider_StarRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserConsultAppointmentRequest
        fields = [
            "consultant_provider_starratting",
            "consultant_provider_starratting_comment",
        ]


class AppointmentSeeker_MissingAppointmentReasonSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserConsultAppointmentRequest
        fields = ["reason_for_missing_appointment"]


class GetSpecificCategoryServiceSearchDataSerializer(serializers.ModelSerializer):
    user_id = serializers.CharField(source="userid.userid")

    class Meta:
        model = ConsultancyCreate
        fields = [
            "id",
            "consultant_service_category",
            "consultant_name",
            "consultant_service_locationcountry",
            "user_id",
        ]


class ConsultancyPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConsultancyPayment
        fields = ["userid", "consultancy_sheduleid", "tran_id"]


class ServiceSearchFilterSerializer(serializers.ModelSerializer):
    user_id = serializers.CharField(source="userid.user_fullname")

    class Meta:
        model = ConsultancyCreate
        fields = [
            "id",
            "consultant_service_category",
            "consultant_name",
            "consultant_service_locationcountry",
            "user_id",
        ]
