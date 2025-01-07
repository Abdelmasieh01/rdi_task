from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveAPIView, RetrieveDestroyAPIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UploadSerializer, ImageDetailSerializer, PdfDetailSerializer, ImageSerializer, PdfSerializer
from .models import Image, Pdf


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
                return Response("Invlid file.", status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def create_image(name, properties, file):
    width = properties["width"]
    height = properties["height"]
    channels = properties["channels"]
    image = Image(name=name, width=width, height=height,
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
        queryset = Image.objects.all()
        name = self.request.query_params.get("name")
        channels = self.request.query_params.get("channels")

        if name:
            queryset = queryset.filter(name__icontains=name)
        if channels:
            queryset = queryset.filter(channels=channels)

        return queryset


class ImageRetreiveDestroyView(RetrieveDestroyAPIView):
    queryset = Image.objects.all()
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
