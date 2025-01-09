import pytest
from rest_framework.test import APIClient
from rest_framework.reverse import reverse
from api.models import Image, Pdf

@pytest.fixture(scope="module")
def url():
    return reverse("api:upload-files")

@pytest.mark.django_db
def test_upload_valid_image(api_client: APIClient, valid_image_base64, url):
    payload = {
        "name": "test-image",
        "file_type": "image",
        "file_data": valid_image_base64
    }

    response = api_client.post(url, payload, format="json")
    data = response.data["data"]
    assert response.status_code == 201
    assert data["name"] == "test-image"
    assert data["width"] == 1
    assert data["height"] == 1
    assert data["channels"] == 4
    assert "file" in data
    assert data["file"].endswith(".png")
    assert Image.objects.count() == 1

@pytest.mark.django_db
def test_upload_valid_pdf(api_client: APIClient, valid_pdf_base64, url):
    payload = {
        "name": "test-pdf",
        "file_type": "pdf",
        "file_data": valid_pdf_base64
    }

    response = api_client.post(url, payload, format="json")
    data = response.data["data"]
    assert response.status_code == 201
    assert data["name"] == "test-pdf"
    assert data["width"] == 595
    assert data["height"] == 842
    assert data["page_count"] == 1
    assert "file" in data
    assert data["file"].endswith(".pdf")
    assert Pdf.objects.count() == 1

@pytest.mark.django_db
def test_upload_invalid_base64(api_client: APIClient, url):
    payload = {
        "name": "test-image",
        "file_type": "image",
        "file_data": "data:image/png;base64,InvalidBase64String"
    }
    response = api_client.post(url, payload, format="json")
    
    assert response.status_code == 400
    assert "file_data" in response.data # This means the file_data field had validation error

@pytest.mark.django_db
def test_upload_invalid_type(api_client: APIClient, url):
    payload = {
        "name": "test-doc",
        "file_type": "document",
        "file_data": "Any Data"
    }
    response = api_client.post(url, payload, format="json")

    assert response.status_code == 400
    assert "file_type" in response.data