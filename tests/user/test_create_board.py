import pytest
from rest_framework.permissions import IsAuthenticated


@pytest.mark.django_db
def test_create_board(user, user_auth_client,topic,client):
    permission_classes = [IsAuthenticated]
    topic = topic.first()

    data = dict(
       topic=topic.id,
    )
    response = client.post("/user/create-board/", data)

    assert response.status_code == 201

    data = dict(
        topic=3,
    )
    response = client.post("/user/create-board/", data)

    assert response.status_code == 400

    data = dict(
    )
    response = client.post("/user/create-board/", data)

    assert response.status_code == 400
