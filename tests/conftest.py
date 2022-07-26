import pytest

from image_post.models import ImageStore
from tests.post.test_image_upload import upload_img
from topic.models import Topic
from user.models import RegisterUser, Boards, FollowPeople
from rest_framework.test import APIClient
from user.token import get_tokens_for_user
from datetime import date


@pytest.fixture
def user():
    data = dict(
        username='Niraj',
        first_name='Niraj',
        last_name='Patel',
        email='niraj@gmail.com',
        password='Niraj2001',
        country='India',
        gender='Male'
    )
    user = RegisterUser.objects.create_user(**data)
    return user


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def admin_user():
    data = dict(
        username='niraj',
        first_name='Niraj',
        last_name='Patel',
        email='nirajadmin@gmail.com',
        password='Admin2001',
        country='India',
        gender='Male',
    )
    user = RegisterUser.objects.create_superuser(**data)
    return user


@pytest.fixture
def user_auth_client(user, client):
    response = client.post('/user/login/', dict(email=user.email, password='Niraj2001'))
    token = get_tokens_for_user(user)
    client.credentials(HTTP_AUTHORIZATION="Bearer " + token["access"])
    return client


@pytest.fixture
def admin_auth_client(admin_user, client):
    response = client.post('/user/login/', dict(email=admin_user.email, password='Admin2001'))
    token = get_tokens_for_user(admin_user)
    client.credentials(HTTP_AUTHORIZATION="Bearer " + token["access"])
    return client


@pytest.fixture
def topic():
    data = dict(
        id=1,
        topic_name='Car'
    )
    Topic.objects.create(**data)
    # data = dict(
    #     topic_name='Bike'
    # )
    # Topic.objects.create(**data)
    topic = Topic.objects.all()
    return topic


@pytest.fixture
def image_upload(user, topic):
    data = dict(
        id=1,
        description='Hello',
        image_path=upload_img(),
        image_upload_date=date.today(),
        image_type='Public',
        approve_status=True,
        user=user,
    )
    image_post = ImageStore.objects.create(**data)
    for topics in topic:
        image_post.topic.add(topics.id)
    return image_post


@pytest.fixture
def create_board(user, user_auth_client, topic):
    first_topic = topic.first()
    data = dict(
        id=1,
        user=user,
        topic=first_topic,
    )
    board = Boards.objects.create(**data)
    # for topics in topic:
    #     board.topic.add(topics.id)
    # data = dict(
    #     user=user,
    #     topic=topic
    # )
    # Boards.objects.create(**data)
    # board = Boards.objects.all()
    return board

@pytest.fixture
def user_follow(second_user, user, second_user_auth_client, client):
    data = dict(
        follower=second_user,
        following=user
    )
    follow_user = FollowPeople.objects.create(**data)
    return follow_user
