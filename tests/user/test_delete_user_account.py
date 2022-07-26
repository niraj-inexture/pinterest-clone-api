import pytest
from rest_framework.permissions import IsAuthenticated


@pytest.mark.django_db
def test_user_delete(user, user_auth_client, client):
    permission_classes = [IsAuthenticated]

    response = client.delete("/user/delete-user-account/")
    # data = response.data
    # print(data)

    assert response.status_code == 200


