import pytest
from django.contrib.auth import get_user_model
from account.models import Account

User = get_user_model()


@pytest.fixture(scope='function')
def test_password():
    return 'strong-test-password'


@pytest.fixture(scope='function')
def create_user(db, django_user_model, test_password):
    def make_user(**kwargs):
        kwargs.setdefault('username', 'testuser')
        kwargs.setdefault('email', 'testuser@example.com')
        user = django_user_model.objects.create_user(**kwargs)
        user.set_password(test_password)
        user.save()
        return user
    return make_user


@pytest.fixture(scope='function')
def auto_login_user(db, client, create_user, test_password):
    def make_auto_login(user=None):
        if user is None:
            user = create_user()
        client.login(username=user.username, password=test_password)
        return client, user
    return make_auto_login


@pytest.fixture(scope='function')
def test_user(db, create_user):
    return create_user()


@pytest.fixture(scope='function')
def authenticated_client(db, client, test_user, test_password):
    client.login(username=test_user.username, password=test_password)
    return client
