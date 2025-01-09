import pytest
from rest_framework.test import APIClient
from rest_framework.reverse import reverse
from api.models import Image
from utils import get_file

@pytest.fixture(scope="function")
@pytest.mark.django_db
def sample_images():
    image_file = get_file("sample-image.png")
    for i in range(5):
        name = f"sample-image-{i+1}"
        image = Image(name=name, width=1, height=1, channels=4)
        image.file.save(name=f"{name}.png", content=image_file, save=False)
        image.save()

@pytest.mark.django_db
def test_get_image_list(api_client: APIClient, sample_images):
    url = reverse("api:images")
    response = api_client.get(url)

    first_image = response.data[0]
    assert response.status_code == 200
    assert len(response.data) == 5
    assert first_image["id"] == 1
    assert first_image["name"] == "sample-image-1"
    assert first_image["channels"] == 4

@pytest.mark.django_db
def test_image_list_filters(api_client: APIClient, sample_images):
    url = reverse("api:images")

    # Searching the name attribute contains 1
    response = api_client.get(url, {"name": "1"})
    assert response.status_code == 200
    assert len(response.data) == 1

    # Searching the channels parameter
    response = api_client.get(url, {"channels": 4})
    assert response.status_code == 200
    assert len(response.data) == 5

@pytest.mark.django_db
def test_get_image(api_client: APIClient, sample_images):
    url = reverse("api:image", kwargs={"pk": 1})
    response = api_client.get(url)
    
    assert response.status_code == 200
    assert response.data["id"] == 1
    assert response.data["name"] == "sample-image-1"
    assert response.data["channels"] == 4

@pytest.mark.django_db
def test_delete_image(api_client: APIClient, sample_images):
    url = reverse("api:image", kwargs={"pk": 1})
    response = api_client.delete(url)
    
    assert response.status_code == 204
    # One deleted image so there will be 4 more
    assert Image.objects.count() == 4