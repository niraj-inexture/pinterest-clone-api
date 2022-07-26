import pytest


@pytest.fixture
def trending_topic(user, user_auth_client, topic):
    trending_topic = topic.first()
    return trending_topic

