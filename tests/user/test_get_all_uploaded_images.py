import pytest
from rest_framework.permissions import IsAuthenticated


@pytest.mark.django_db
def test_get_all_image(user, user_auth_client, image_upload,client):
    permission_classes = [IsAuthenticated]

    response = client.get("/user/home/")

    data = response.data
    print(data)

    assert response.status_code == 200