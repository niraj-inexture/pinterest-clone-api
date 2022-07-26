import pytest
from rest_framework.permissions import IsAuthenticated


@pytest.mark.django_db
def test_image_detail(user,user_auth_client,image_upload,create_board,create_comment,image_like,user_follow,client):
    permission_classes = [IsAuthenticated]

    response = client.get("/image/image-detail/1")
    data = response.data
    print(data)

    assert response.status_code == 200

