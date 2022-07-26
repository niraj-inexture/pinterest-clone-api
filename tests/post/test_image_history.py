import pytest
from rest_framework.permissions import IsAuthenticated


@pytest.mark.django_db
def test_image_history(user, user_auth_client, image_upload, client):
    permission_classes = [IsAuthenticated]

    response = client.get("/image/image-history/")
    data = response.data
    print(data)
    assert response.status_code == 200


@pytest.mark.django_db
def test_image_history_for_second_user(second_user, second_user_auth_client, image_upload, client):
    permission_classes = [IsAuthenticated]

    response = client.get("/image/image-history/")
    data = response.data
    print(data)
    assert response.status_code == 400
