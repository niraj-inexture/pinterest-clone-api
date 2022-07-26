import pytest
from rest_framework.permissions import IsAuthenticated

from tests.post.test_image_upload import upload_img
from user.models import RegisterUser


@pytest.mark.django_db
def test_update_user_profile(user, user_auth_client,client):

    permission_classes = [IsAuthenticated]

    data = dict(
        username='kevin',
        first_name='Kevin',
        last_name='Patel',
        email='kevin@gmail.com',
        password='Kevin2001',
        country='India',
        gender='Male',
        profile_image=upload_img()
    )
    user = RegisterUser.objects.create_user(**data)

    data = dict(
        username='niraj',
        first_name='Niraj',
        last_name='Patel',
        email='niraj123@gmail.com',
        password='Niraj2001',
        country='India',
        gender='Male',
        profile_image=upload_img()
    )
    response = client.patch("/user/profile-update/", data)

    assert response.status_code == 200

    data = dict(
        username='kevin',
        first_name='Niraj',
        last_name='Patel',
        email='niraj@gmail.com',
        password='Niraj2001',
        country='India',
        gender='Male',
        profile_image=upload_img()
    )
    response = client.patch("/user/profile-update/", data)

    assert response.status_code == 400

    data = dict(
        username='niraj',
        first_name='Niraj',
        last_name='Patel',
        email='kevin@gmail.com',
        password='Niraj2001',
        country='India',
        gender='Male',
        profile_image=upload_img()
    )
    response = client.patch("/user/profile-update/", data)

    assert response.status_code == 400