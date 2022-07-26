import pytest
from rest_framework.permissions import IsAuthenticated


@pytest.mark.django_db
def test_delete_comment(user, user_auth_client, image_upload,create_comment, client):
    permission_classes = [IsAuthenticated]

    response = client.delete("/image/delete-comment/1")
    # data = response.data
    # print(data)
    assert response.status_code == 200

    response = client.delete("/image/delete-comment/3")
    # data = response.data
    # print(data)
    assert response.status_code == 404
