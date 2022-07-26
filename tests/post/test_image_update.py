import pytest
from rest_framework.permissions import IsAuthenticated

from topic.models import Topic


@pytest.mark.django_db
def test_image_update(user, user_auth_client, image_upload, client):
    permission_classes = [IsAuthenticated]

    topic = Topic.objects.all()
    data = dict(
        description='Hello',
    )
    for topics in topic:
        image_upload.topic.add(topics.id)
    response = client.patch("/image/image-update/1", data)
    assert image_upload.description == "Hello"
    assert response.status_code == 200

    data = dict(
        id=2,
        topic_name="cars",
    )
    single_topic = Topic.objects.create(**data)

    data = dict(
        description='Hello',
        topic=single_topic.id
    )
    response = client.patch("/image/image-update/1", data)
    assert image_upload.description == "Hello"
    assert response.status_code == 200

    data = dict(
        description='Hello',
        topic=single_topic.id
    )
    response = client.patch("/image/image-update/3", data)
    assert image_upload.description == "Hello"
    assert response.status_code == 400

    data = dict(
    )
    response = client.patch("/image/image-update/3", data)
    assert response.status_code == 400

