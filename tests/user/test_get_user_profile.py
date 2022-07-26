import pytest
from rest_framework.permissions import IsAuthenticated


@pytest.mark.django_db
def test_get_user_profile(user, user_auth_client, client):
    permission_classes = [IsAuthenticated]
    response = client.get("/user/user-profile/")

    # data = response.data
    # print(data)

    assert response.status_code == 200
