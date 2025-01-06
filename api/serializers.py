from rest_framework import serializers
from .models import Image as ImageModel, Pdf
import base64, uuid
from PIL import Image
from PyPDF2 import PdfReader
from django.core.files.base import ContentFile


class UploadSerializer(serializers.Serializer):
    name = serializers.CharField()
    file_type = serializers.ChoiceField(choices=["pdf", "image"])
    file_data = serializers.CharField()

    def validate_file_data(self, value):
        try:
            # Get the format and file string from the string
            format, filestr = value.split(';base64,')
            # Decode the base64 data into a file
            decoded_file = base64.b64decode(filestr)
            # Get the extension from the format text
            ext = format.split("/")[1]
            # Return as file object
            file_object = ContentFile(decoded_file, name=uuid.uuid4().urn[9:] + '.' + ext)
            return file_object
        except Exception as e:
            print(e.__str__())
            raise serializers.ValidationError("Invalid base64 string.")

    def get_file_properties(self, file_type, file_object):
        if file_type == "image":
            with Image.open(file_object) as img:
                width, height = img.size
                # Get the length of bands in the image to know how many channels
                channels = len(img.getbands())
                return {"width": width, "height": height, "channels": channels}
        elif file_type == "pdf":
            reader = PdfReader(file_object)
            page = reader.pages[0]
            width = page.mediabox.width
            height = page.mediabox.height
            page_count = len(reader.pages)
            return {"width": width, "height": height, "page_count": page_count}
        else:
            raise serializers.ValidationError("Unsupported file type.")


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageModel
        fields = ["id", "name", "channels", "file"]


class ImageDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageModel
        fields = ["id", "name", "file", "height", "width",
                  "channels", "created_at", "modified_at"]


class PdfSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pdf
        fields = ["id", "name", "page_count", "file"]


class PdfDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pdf
        fields = ["id", "name", "file", "height", "width",
                  "page_count", "created_at", "modified_at"]
