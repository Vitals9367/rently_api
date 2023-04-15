import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import AccessToken


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def user():
    user = User.objects.create_user(
        username='testuser',
        email='testuser@example.com',
        password='testpass'
    )

    return user


@pytest.fixture
def authenticated_user():
    user = User.objects.create_user(
        username='testuser', password='testpassword'
    )
    acces_token = AccessToken.for_user(user)

    return user, str(acces_token)
