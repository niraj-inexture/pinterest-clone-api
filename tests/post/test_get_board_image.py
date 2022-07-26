import pytest
from rest_framework.permissions import IsAuthenticated


@pytest.mark.django_db
def test_get_board_image(user, user_auth_client, image_upload,save_image_in_board,create_board, client):
    permission_classes = [IsAuthenticated]

    response = client.get("/image/board-images/1")
    # data = response.data
    # print(data)

    assert response.status_code == 200

    response = client.get("/image/board-images/2")
    # data = response.data
    # print(data)

    assert response.status_code == 404

