import pytest
from rest_framework.permissions import IsAuthenticated


@pytest.mark.django_db
def test_delete_board_image(user, user_auth_client, image_upload, create_board,save_image_in_board, client):
    permission_classes = [IsAuthenticated]

    response = client.delete("/image/delete-board-image/1/1")
    data = response.data
    print(data)
    assert response.status_code == 200

    response = client.delete("/image/delete-board-image/2/1")
    data = response.data
    print(data)
    assert response.status_code == 400

    response = client.delete("/image/delete-board-image/1/5")
    data = response.data
    print(data)
    assert response.status_code == 400
