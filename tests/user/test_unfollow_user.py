import pytest
from rest_framework.permissions import IsAuthenticated


@pytest.mark.django_db
def test_user_unfollow(user, second_user,second_user_auth_client,user_follow, client):
    permission_classes = [IsAuthenticated]

    data = dict(
        following=user.id,
    )
    response = client.delete("/user/unfollow/",data)
    assert response.status_code == 200

    data = dict(
    )
    response = client.delete("/user/unfollow/", data)
    assert response.status_code == 400

    data = dict(
        following=second_user.id,
    )
    response = client.delete("/user/unfollow/", data)
    assert response.status_code == 400
