import pytest
from rest_framework.permissions import IsAuthenticated


@pytest.mark.django_db
def test_update_comment(user, user_auth_client, image_upload, create_comment, client):
    permission_classes = [IsAuthenticated]

    data = dict(
        image_path=image_upload.id,
        comment="Nice"
    )

    response = client.put("/image/update-comment/1",data)
    data = response.data
    print(data)
    assert response.status_code == 200

    data = dict(
        image_path=image_upload.id,
        comment="Nice"
    )

    response = client.delete("/image/update-comment/3")
    data = response.data
    print(data)
    assert response.status_code == 404
