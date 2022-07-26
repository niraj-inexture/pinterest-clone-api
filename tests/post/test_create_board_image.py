import pytest
from rest_framework.permissions import IsAuthenticated


@pytest.mark.django_db
def test_create_board_image(user, user_auth_client, image_upload,create_board, client):
    permission_classes = [IsAuthenticated]
   
    data = dict(
        image_post=image_upload.id,
        topic=create_board.id
    )

    response = client.post("/image/board-save-image/",data)
    # data = response.data
    # print(data)
    assert response.status_code == 200

    data = dict(
        image_post=image_upload.id,
        topic=create_board.id
    )

    response = client.post("/image/board-save-image/", data)
    # data = response.data
    # print(data)
    assert response.status_code == 400

    data = dict(
        image_post=image_upload.id,
        topic=10
    )

    response = client.post("/image/board-save-image/", data)
    # data = response.data
    # print(data)
    assert response.status_code == 400

    data = dict(
    )

    response = client.post("/image/board-save-image/", data)
    # data = response.data
    # print(data)
    assert response.status_code == 400
