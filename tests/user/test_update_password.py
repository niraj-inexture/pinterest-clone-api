import pytest
from rest_framework.permissions import IsAuthenticated


@pytest.mark.django_db
def test_update_user_password(user, user_auth_client,client):

    permission_classes = [IsAuthenticated]

    data = dict(
        password='Niraj2001',
        new_password='niraj2001'
    )
    response = client.put("/user/update-password/", data)
    # data = response.data
    # print(data)

    assert response.status_code == 200

    data = dict(
        password='Niraj2001',
        new_password='niraj2001'
    )
    response = client.put("/user/update-password/", data)
    # data = response.data
    # print(data)

    assert response.status_code == 400

    data = dict(
    )
    response = client.put("/user/update-password/", data)
    # data = response.data
    # print(data)

    assert response.status_code == 400
