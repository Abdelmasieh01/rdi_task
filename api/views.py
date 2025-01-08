from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveDestroyAPIView
from rest_framework.response import Response
from rest_framework import status
from django.core.files.base import ContentFile
from .serializers import UploadSerializer, ImageDetailSerializer, PdfDetailSerializer, ImageSerializer, PdfSerializer, RotateImageSerializer
from .models import Image as ImageModel, Pdf
from PIL import Image
from io import BytesIO
from uuid import uuid4


class UploadView(APIView):
    def post(self, request):
        serializer = UploadSerializer(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            file_type = validated_data["file_type"]
            file_object = validated_data["file_data"]
            name = validated_data["name"]

            # Get file properties
            properties = serializer.get_file_properties(file_type, file_object)
            try:
                if file_type == "image":
                    image = create_image(name, properties, file_object)
                    image_item = ImageDetailSerializer(instance=image)
                    return Response({"message": "Image created successfully!", "data": image_item.data}, status=status.HTTP_201_CREATED)
                elif file_type == "pdf":
                    pdf = create_pdf(name, properties, file_object)
                    pdf_item = PdfDetailSerializer(instance=pdf)
                    return Response({"message": "PDF created successfully!", "data": pdf_item.data}, status=status.HTTP_201_CREATED)
            except Exception as e:
                print(e.__str__())
                return Response({"message": "Invlid file."}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def create_image(name, properties, file):
    width = properties["width"]
    height = properties["height"]
    channels = properties["channels"]
    image = ImageModel(name=name, width=width, height=height,
                       channels=channels, file=file)
    image.save()
    return image


def create_pdf(name, properties, file):
    width = properties["width"]
    height = properties["height"]
    page_count = properties["page_count"]
    pdf = Pdf(name=name, width=width, height=height,
              page_count=page_count, file=file)
    pdf.save()
    return pdf


class ImageListView(ListAPIView):
    serializer_class = ImageSerializer

    def get_queryset(self):
        queryset = ImageModel.objects.all()
        name = self.request.query_params.get("name")
        channels = self.request.query_params.get("channels")

        if name:
            queryset = queryset.filter(name__icontains=name)
        if channels:
            queryset = queryset.filter(channels=channels)

        return queryset


class ImageRetreiveDestroyView(RetrieveDestroyAPIView):
    queryset = ImageModel.objects.all()
    serializer_class = ImageDetailSerializer


class PdfListView(ListAPIView):
    serializer_class = PdfSerializer

    def get_queryset(self):
        queryset = Pdf.objects.all()
        name = self.request.query_params.get("name")
        page_count = self.request.query_params.get("page_count")

        if name:
            queryset = queryset.filter(name__icontains=name)
        if page_count:
            queryset = queryset.filter(page_count=page_count)

        return queryset


class PdfRetreiveDestroyView(RetrieveDestroyAPIView):
    queryset = Pdf.objects.all()
    serializer_class = PdfDetailSerializer


class RotateImageView(APIView):
    def post(self, request):
        serializer = RotateImageSerializer(data=request.data)
        # The serializer uses a primary key related field so validation will mean that an image with this id is found
        if serializer.is_valid():
            try:
                orig_img = serializer.validated_data["id"]
                rot_angle = serializer.validated_data["rot_angle"]
                img = Image.open(orig_img.file.path)
                format = img.format
                rot_img = img.rotate(angle=rot_angle)
                # Save the rotated image to a BytesIO buffer
                buffer = BytesIO()
                rot_img.save(buffer, format=format)
                buffer.seek(0)

                rot_img_name = orig_img.name + " - rotation: " + str(rot_angle)
                rot_img_file = ContentFile(
                    buffer.read(), name=uuid4().urn[9:] + '.' + format)
                
                rot_img_obj = ImageModel(
                    name=rot_img_name, width=orig_img.width, height=orig_img.height,
                    file=rot_img_file, channels=orig_img.channels)
                rot_img_obj.save()
                rot_img_item = ImageSerializer(instance=rot_img_obj)
                return Response({"message": "Image rotated successfully!", "data": rot_img_item.data}, status=status.HTTP_201_CREATED)
            except Exception as e:
                print(e)
                return Response({"message": "Invalid data."}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ConvertPdfToImageView(APIView):
    pass