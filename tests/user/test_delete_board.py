import pytest
from rest_framework.permissions import IsAuthenticated


@pytest.mark.django_db
def test_delete_board(user, user_auth_client,create_board, client):
    permission_classes = [IsAuthenticated]

    response = client.delete("/user/delete-board/3")
    assert response.status_code == 404

    response = client.delete("/user/delete-board/1")
    assert response.status_code == 200