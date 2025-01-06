from django.urls import path
from . import views

app_name = "api"

urlpatterns = [
    path('upload/', views.UploadView.as_view(), name='upload-files'),
    path('images/', views.ImageListView.as_view(), name='images'),
    path('pdfs/', views.PdfListView.as_view(), name='pdfs'),
    path('images/<int:pk>/', views.ImageRetreiveView.as_view(), name='get-image'),
    path('pdfs/<int:pk>/', views.PdfRetreiveView.as_view(), name='get-pdf'),
]