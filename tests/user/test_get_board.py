import pytest
from rest_framework.permissions import IsAuthenticated


@pytest.mark.django_db
def test_get_board(user, user_auth_client,create_board, client):
    permission_classes = [IsAuthenticated]

    # response = client.get("/user/get-board/")
    # data = response.data
    # print(data)
    #
    # assert response.status_code == 404

    response = client.get("/user/get-board/")
    # data = response.data
    # print(data)

    assert response.status_code == 200