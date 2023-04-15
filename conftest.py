import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def test_user():
    password = 'testpass'
    user = User.objects.create_user(
        username='testuser',
        email='testuser@example.com',
        password=password
    )

    user.password = password
    return user


@pytest.fixture
def authenticated_test_user(test_user):
    refresh_token = RefreshToken.for_user(test_user)
    return test_user, str(refresh_token.access_token), str(refresh_token)
