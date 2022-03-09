from asyncio.log import logger
from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField, Base64FileField
from .models import ConsultancyCreate
import PyPDF2
import io

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


class SearchServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConsultancyCreate
        fields = '__all__'








