from asyncio.log import logger
from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField, Base64FileField
from .models import ConsultancyCreate
from auth_user_app.models import User
import PyPDF2
import io
from user_connection_app.serializers import UserEducationSerializer

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




class UserDataConsultancySerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_industry', 'user_geolocation']

class SearchServiceSerializer(serializers.ModelSerializer):
    user_educationdata = UserEducationSerializer(many=True, read_only=True)
    # user_data = UserDataConsultancySerializer(many=True, read_only=True)
    class Meta:
        model = ConsultancyCreate
        fields = [ 'id', 'user_educationdata', 'consultant_name']








