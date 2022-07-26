import pytest


@pytest.mark.django_db
def test_search(user, user_auth_client, client, topic, image_upload):
    data = dict(
        search='Car'
    )

    response = client.get("/user/search/", data)
    assert response.status_code == 200

    data = dict(
        search=" "
    )

    response = client.get("/user/search/", data)
    assert response.status_code == 400
