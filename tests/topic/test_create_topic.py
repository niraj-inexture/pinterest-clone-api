import pytest
from rest_framework.permissions import IsAdminUser


@pytest.mark.django_db
def test_create_topic(admin_auth_client,client):
    permission_classes = [IsAdminUser]

    data = dict(
        topic_name='Car',
        total_likes=10
    )
    response = client.post("/topic/create-topic/", data)

    assert response.status_code == 200

    data = dict(
        topic_name='Car',
    )
    response = client.post("/topic/create-topic/", data)

    assert response.status_code == 200

    data = dict(
        total_likes=10
    )
    response = client.post("/topic/create-topic/", data)

    assert response.status_code == 400
