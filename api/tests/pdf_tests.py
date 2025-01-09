import pytest
from rest_framework.test import APIClient
from rest_framework.reverse import reverse
from api.models import Pdf
from utils import get_file

@pytest.fixture
@pytest.mark.django_db
def sample_pdfs():
    pdf_file = get_file("sample-pdf.pdf")
    for i in range(5):
        name = f"sample-pdf-{i+1}"
        image = Pdf(name=name, width=1, height=1, page_count=1)
        image.file.save(name=f"{name}.pdf", content=pdf_file, save=False)
        image.save()

@pytest.mark.django_db
def test_get_pdf_list(api_client: APIClient, sample_pdfs):
    url = reverse("api:pdfs")
    response = api_client.get(url)

    first_image = response.data[0]
    assert response.status_code == 200
    assert len(response.data) == 5
    assert first_image["id"] == 1
    assert first_image["name"] == "sample-pdf-1"
    assert first_image["page_count"] == 1

@pytest.mark.django_db
def test_pdf_list_filters(api_client: APIClient, sample_pdfs):
    url = reverse("api:pdfs")

    # Searching the name attribute contains 1
    response = api_client.get(url, {"name": "1"})
    assert response.status_code == 200
    assert len(response.data) == 1

    # Searching the channels parameter
    response = api_client.get(url, {"page_count": 1})
    assert response.status_code == 200
    assert len(response.data) == 5

@pytest.mark.django_db
def test_get_pdf(api_client: APIClient, sample_pdfs):
    url = reverse("api:pdf", kwargs={"pk": 1})
    response = api_client.get(url)
    
    assert response.status_code == 200
    assert response.data["id"] == 1
    assert response.data["name"] == "sample-pdf-1"
    assert response.data["page_count"] == 1

@pytest.mark.django_db
def test_delete_pdf(api_client: APIClient, sample_pdfs):
    url = reverse("api:pdf", kwargs={"pk": 1})
    response = api_client.delete(url)
    
    assert response.status_code == 204
    # One deleted image so there will be 4 more
    assert Pdf.objects.count() == 4