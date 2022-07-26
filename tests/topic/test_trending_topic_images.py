import pytest
from rest_framework.permissions import IsAdminUser


@pytest.mark.django_db
def test_trending_topic_images(user, user_auth_client, image_upload,topic, trending_topic, client):

    data = dict(
        topic_id=trending_topic.id
    )

    response = client.get("/topic/trending-topic-images/", data)
    data = response.data
    print(data)

    assert response.status_code == 400
