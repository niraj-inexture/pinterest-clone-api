import pytest


@pytest.mark.django_db
def test_search_list(user, user_auth_client, topic, client):
    response = client.get("/user/topic-list/")
    assert response.status_code == 200
