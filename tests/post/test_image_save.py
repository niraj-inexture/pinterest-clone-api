import pytest
from rest_framework.permissions import IsAuthenticated


@pytest.mark.django_db
def test_image_save(user, user_auth_client, image_upload, client):
    permission_classes = [IsAuthenticated]

    data=dict(
        image_path=image_upload.id
    )
    response = client.post("/image/image-save/", data)
    assert response.status_code == 200

    data = dict(
        image_path=3
    )
    response = client.post("/image/image-save/", data)
    # data = response.data
    # print(data)
    assert response.status_code == 400

    data = dict(
    )
    response = client.post("/image/image-save/", data)
    # data = response.data
    # print(data)
    assert response.status_code == 400