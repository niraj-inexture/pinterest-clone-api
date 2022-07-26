import pytest
from rest_framework.permissions import IsAuthenticated


@pytest.mark.django_db
def test_image_unlike(user, user_auth_client, image_upload,image_like, client):
    permission_classes = [IsAuthenticated]

    data=dict(
        image_id=image_upload.id
    )
    response = client.delete("/image/image-unlike/", data)
    assert response.status_code == 200

    data = dict(
        image_id=4
    )
    response = client.delete("/image/image-unlike/", data)
    assert response.status_code == 400

    data = dict(
    )
    response = client.delete("/image/image-unlike/", data)
    assert response.status_code == 400


@pytest.mark.django_db
def test_not_like(user,user_auth_client,image_upload,client):
    permission_classes = [IsAuthenticated]

    data = dict(
        image_id=image_upload.id
    )
    response = client.delete("/image/image-unlike/", data)
    assert response.status_code == 400
