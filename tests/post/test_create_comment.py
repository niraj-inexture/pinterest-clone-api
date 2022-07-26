import pytest
from rest_framework.permissions import IsAuthenticated


@pytest.mark.django_db
def test_create_comment(user, user_auth_client, image_upload, client):
    permission_classes = [IsAuthenticated]
    data = dict(
        image_path=image_upload.id,
        comment="Nice"
    )

    response = client.post("/image/create-comment/",data)
    # data = response.data
    # print(data)
    assert response.status_code == 201

    data = dict(
        image_path=15,
        comment="Nice"
    )

    response = client.post("/image/create-comment/", data)
    # data = response.data
    # print(data)
    assert response.status_code == 400

    data = dict(
    )

    response = client.post("/image/create-comment/", data)
    # data = response.data
    # print(data)
    assert response.status_code == 400
