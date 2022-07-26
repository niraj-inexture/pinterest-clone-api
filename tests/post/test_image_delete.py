import pytest
from rest_framework.permissions import IsAuthenticated


@pytest.mark.django_db
def test_delete_image(user,user_auth_client, client, image_upload):
    permission_classes = [IsAuthenticated]

    data = dict(
        image_id=image_upload.id,
        user=user.id
    )

    response = client.delete("/image/image-delete/", data)
    assert response.status_code == 200

    data = dict(
        image_id=10,
        user=user.id
    )

    response = client.delete("/image/image-delete/", data)
    assert response.status_code == 400
