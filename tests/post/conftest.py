import pytest

from image_post.models import ImageLike, ImageSave, Comment, BoardImages
from user.models import RegisterUser
from user.token import get_tokens_for_user


@pytest.fixture
def image_like(user, user_auth_client, image_upload, client):
    data = dict(
        user=image_upload.user,
        image_path=image_upload,
        like_user=user
    )

    like_img = ImageLike.objects.create(**data)
    return like_img


@pytest.fixture
def image_save(user, user_auth_client, image_upload, client):
    data = dict(
        user=user,
        image_path=image_upload,
    )

    save_img = ImageSave.objects.create(**data)
    return save_img


@pytest.fixture
def create_comment(user, user_auth_client, image_upload, client):
    data = dict(
        id=1,
        user=user,
        image_path=image_upload,
        comment="good"
    )
    comment = Comment.objects.create(**data)
    return comment


@pytest.fixture
def save_image_in_board(user, user_auth_client, image_upload,topic, create_board, client):
    data = dict(
        id=1,
        user=user,
        image_post=image_upload,
        topic=create_board.topic
    )
    board_image = BoardImages.objects.create(**data)

    return board_image


@pytest.fixture
def second_user():
    data = dict(
        id=3,
        username='ashok',
        first_name='Ashok',
        last_name='Patel',
        email='ashok@gmail.com',
        password='Ashok2001',
        country='India',
        gender='Male'
    )
    second_user = RegisterUser.objects.create_user(**data)
    return second_user


@pytest.fixture
def second_user_auth_client(second_user, client):
    response = client.post('/user/login/', dict(email=second_user.email, password='Ashok2001'))
    token = get_tokens_for_user(second_user)
    client.credentials(HTTP_AUTHORIZATION="Bearer " + token["access"])
    return client
