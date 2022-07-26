import pytest

from user.models import RegisterUser, FollowPeople
from user.token import get_tokens_for_user


@pytest.fixture
def second_user():
    data = dict(
        id=2,
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


@pytest.fixture
def deactivate_user():
    data = dict(
        id=2,
        username='ashok',
        first_name='Ashok',
        last_name='Patel',
        email='pareshmalukani99@gmail.com',
        password='Ashok2001',
        country='India',
        gender='Male',
        is_active=False
    )
    deactivate_user = RegisterUser.objects.create_user(**data)
    return deactivate_user
