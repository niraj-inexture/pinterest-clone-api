import pytest


@pytest.mark.django_db
def test_activate_account(deactivate_user, client):
    data = dict(
        email=deactivate_user.email
    )

    response = client.post("/user/activate-account/", data)
    # data = response.data
    # print(data)

    assert response.status_code == 200


@pytest.mark.django_db
def test_already_activate_account(user, client):
    data = dict(
        email=user.email
    )

    response = client.post("/user/activate-account/", data)
    # data = response.data
    # print(data)

    assert response.status_code == 400
