import pytest


@pytest.mark.django_db
def test_send_password_reset_email_to_deactivate_user(deactivate_user, client):
    data = dict(
        email=deactivate_user.email
    )

    response = client.post("/user/password-reset/", data)
    data = response.data
    print(data)

    assert response.status_code == 400


@pytest.mark.django_db
def test_send_password_reset_email(user, client):
    data = dict(
        email=user.email
    )

    response = client.post("/user/password-reset/", data)
    data = response.data
    print(data)

    assert response.status_code == 200