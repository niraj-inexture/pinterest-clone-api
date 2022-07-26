import pytest
from rest_framework.permissions import IsAdminUser


@pytest.mark.django_db
def test_trending_topic(user,user_auth_client,topic,client):
    permission_classes = [IsAdminUser]

    response = client.get("/topic/trending-topics/")
    data = response.data
    print(data)

    assert response.status_code == 200


@pytest.mark.django_db
def test_trending_topic_not_available(user, user_auth_client, client):
    permission_classes = [IsAdminUser]

    response = client.get("/topic/trending-topics/")
    data = response.data
    print(data)

    assert response.status_code == 400



