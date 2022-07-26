import pytest
from rest_framework.permissions import IsAdminUser


@pytest.mark.django_db
def test_delete_topic(admin_auth_client, client, topic):
    permission_classes = [IsAdminUser]

    response = client.delete("/topic/delete-topic/1")
    assert response.status_code == 200

    response = client.delete("/topic/delete-topic/2")
    assert response.status_code == 404
