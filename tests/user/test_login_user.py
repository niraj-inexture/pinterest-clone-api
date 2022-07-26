import pytest


@pytest.mark.django_db
def test_login_user_success(user, client):
    data=dict(
        email=user.email,
        password='Niraj2001'
    )

    response = client.post("/user/login/", data)

    assert response.status_code == 200



@pytest.mark.django_db
def test_login_user_fail(user, client):
    data=dict(
        email=user.email,
        password='kevin'
    )

    response = client.post("/user/login/", data)

    assert response.status_code == 400


@pytest.mark.django_db
def test_login_user_field_miss_password(user, client):
    data=dict(
        email=user.email,
    )

    response = client.post("/user/login/", data)

    assert response.status_code == 400


@pytest.mark.django_db
def test_login_user_field_miss_email(user, client):
    data=dict(
        password='Niraj2001',
    )

    response = client.post("/user/login/", data)

    assert response.status_code == 400


@pytest.mark.django_db
def test_login_user_both_field_miss(user, client):
    data=dict(
    )

    response = client.post("/user/login/", data)

    assert response.status_code == 400


@pytest.mark.django_db
def test_deactive_login_account(deactivate_user, client):
    data=dict(
        email=deactivate_user.email,
        password='Ashok2001'
    )

    response = client.post("/user/login/", data)

    assert response.status_code == 400



