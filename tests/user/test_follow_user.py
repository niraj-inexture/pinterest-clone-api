import pytest
from rest_framework.permissions import IsAuthenticated


@pytest.mark.django_db
def test_user_follow(second_user, user_auth_client, client):
    permission_classes = [IsAuthenticated]

    data = dict(
        follower=second_user.id
    )
    response = client.post("/user/follow/", data)
    assert response.status_code == 200

    data = dict(
    )
    response = client.post("/user/follow/", data)
    assert response.status_code == 400

    data = dict(
        follower=3
    )
    response = client.post("/user/follow/", data)
    assert response.status_code == 400
