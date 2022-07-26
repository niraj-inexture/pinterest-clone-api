import pytest

from tests.post.test_image_upload import upload_img


@pytest.mark.django_db
def test_register_user(client):
    data = dict(
        username='Niraj',
        first_name='Niraj',
        last_name='Patel',
        email='niraj@gmal.com',
        password='Niraj2001',
        country='India',
        gender='Male',
        profile_image=upload_img()
    )
    response = client.post("/user/register/", data)

    assert response.status_code == 201

    data = dict(
        username='Niraj',
        first_name='Niraj',
        last_name='Patel',
        email='niraj123@gmal.com',
        password='Niraj2001',
        country='India',
        gender='Male'
    )
    response = client.post("/user/register/", data)

    assert response.status_code == 400

    data = dict(
        username='niraj',
        first_name='Niraj',
        last_name='Patel',
        email='niraj@gmal.com',
        password='Niraj2001',
        country='India',
        gender='Male'
    )
    response = client.post("/user/register/", data)

    assert response.status_code == 400

    data = dict(
        username='niraj',
        first_name='Niraj',
        last_name='Patel',
        email='niraj@gmal.com',
        password='Niraj2001',
        country='India',
    )
    response = client.post("/user/register/", data)

    assert response.status_code == 400

    data = dict(
        username='niraj',
        first_name='Niraj12',
        last_name='Patel',
        email='niraj@gmal.com',
        password='Niraj2001',
        country='India',
        gender='Male'
    )
    response = client.post("/user/register/", data)

    assert response.status_code == 400

    data = dict(
        username='niraj',
        first_name='Niraj',
        last_name='Patel@',
        email='niraj@gmal.com',
        password='Niraj2001',
        country='India',
        gender='Male',
        profile_image=upload_img()
    )
    response = client.post("/user/register/", data)

    assert response.status_code == 400

    data = dict(
        username='ashok',
        first_name='Ashok',
        last_name='Patel',
        email='ashok@gmal.com',
        password='Ashok2001',
        country='India',
        gender='Male',
    )
    response = client.post("/user/register/", data)

    assert response.status_code == 201





