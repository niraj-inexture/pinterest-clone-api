import pytest
from rest_framework.permissions import IsAuthenticated


@pytest.mark.django_db
def test_image_unsave(user, user_auth_client, image_upload,image_save, client):
    permission_classes = [IsAuthenticated]

    data=dict(
        image_id=image_upload.id
    )
    response = client.delete("/image/image-unsave/", data)
    # data = response.data
    # print(data)
    assert response.status_code == 200

    data = dict(
        image_id=3
    )
    response = client.delete("/image/image-unsave/", data)
    # data = response.data
    # print(data)
    assert response.status_code == 400

    data = dict(
    )
    response = client.delete("/image/image-unsave/", data)
    # data = response.data
    # print(data)
    assert response.status_code == 400