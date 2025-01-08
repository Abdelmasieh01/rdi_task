from django.urls import path
from . import views

app_name = "api"

urlpatterns = [
    path('upload/', views.UploadView.as_view(), name='upload-files'),
    path('images/', views.ImageListView.as_view(), name='images'),
    path('pdfs/', views.PdfListView.as_view(), name='pdfs'),
    path('images/<int:pk>/', views.ImageRetreiveDestroyView.as_view(), name='get-image'),
    path('pdfs/<int:pk>/', views.PdfRetreiveDestroyView.as_view(), name='get-pdf'),
    path('rotate/', views.RotateImageView.as_view(), name='rot-img')
]