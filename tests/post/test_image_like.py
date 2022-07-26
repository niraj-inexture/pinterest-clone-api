import pytest
from rest_framework.permissions import IsAuthenticated


@pytest.mark.django_db
def test_image_like(user, user_auth_client, image_upload, client):
    permission_classes = [IsAuthenticated]

    data=dict(
        user=image_upload.user.id,
        image_path=image_upload.id
    )
    response = client.post("/image/image-like/", data)
    assert response.status_code == 200

    data = dict(
    )
    response = client.post("/image/image-like/", data)
    assert response.status_code == 400


