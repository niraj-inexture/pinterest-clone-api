from datetime import date
import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.permissions import IsAuthenticated

from topic.models import Topic


def upload_img():
    with open('tests/post/img/image6.jpg', 'rb') as img_file:
        mock_profile_image = SimpleUploadedFile('image6.jpg', img_file.read(), content_type='multipart/form-data')
    return mock_profile_image


def upload_wrong_img():
    with open('tests/post/img/sem8.pdf', 'rb') as img_file:
        mock_profile_image = SimpleUploadedFile('sem8.pdf', img_file.read(), content_type='multipart/form-data')
    return mock_profile_image


@pytest.mark.django_db
def test_image_upload(user, user_auth_client, client):
    permission_classes = [IsAuthenticated]

    data=dict(
        id=2,
        topic_name='ok'
    )
    topic = Topic.objects.create(**data)

    data = dict(
        description='Hello',
        image_path=upload_img(),
        image_upload_date=date.today(),
        image_type='Public',
        user=user,
        topic=topic.id,
    )
    response = client.post("/image/image-upload/", data)
    assert response.status_code == 200

    data = dict(
        description='Hello',
        image_path=upload_img(),
        image_upload_date=date.today(),
        image_type='Private',
        user=user,
        topic=topic.id
    )
    response = client.post("/image/image-upload/", data)
    assert response.status_code == 200

    data = dict(
        description='Hello',
        image_path=upload_img(),
        image_upload_date=date.today(),
        image_type='',
        user=user,
        topic=topic
    )
    response = client.post("/image/image-upload/", data)
    assert response.status_code == 400

    data = dict(
        description='Hello',
        image_path=upload_img(),
        image_upload_date=date.today(),
        image_type='HI',
        user=user,
        topic=topic.id
    )
    response = client.post("/image/image-upload/", data)
    assert response.status_code == 400

    data = dict(
        description='Hello',
        image_path=upload_wrong_img(),
        image_upload_date=date.today(),
        image_type='Private',
        user=user,
        topic=topic.id
    )
    response = client.post("/image/image-upload/", data)
    assert response.status_code == 400

    data = dict(
        description='Hello',
        image_path=upload_img(),
        image_type='Private',
        user=user,
        topic=topic.id
    )
    response = client.post("/image/image-upload/", data)
    assert response.status_code == 200