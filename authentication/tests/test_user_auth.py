import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from django.contrib.auth.models import User
from unittest.mock import patch


@pytest.fixture
def authenticated_github_user():
    with patch('social_core.backends.github.GithubOAuth2.validate_state') as mock_validate_state:
        mock_validate_state.return_value = True
        user = User.objects.create_user(
            username='testuser', password='testpassword', email='testuser@example.com'
        )
        user.social_auth.create(
            provider='github',
            uid='12345',
            extra_data={
                'access_token': 'test_token'
            }
        )
        acces_token = AccessToken.for_user(user)

        yield user, str(acces_token)


@pytest.mark.parametrize("method", ["get", "put", "patch", "delete"])
@pytest.mark.parametrize("endpoint", ["register-user"])
def test_not_allowed_methods(client, method, endpoint):
    assert (getattr(client, method)(reverse(endpoint), format="json").status_code == 405)


@pytest.mark.django_db
def test_jwt_github_authentication(client, authenticated_github_user):
    user, jwt_token = authenticated_github_user
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {jwt_token}')
    url = reverse('test-protected-view')
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_user_registration(client):
    register_url = reverse('register-user')
    data = {
        'username': 'testuser',
        'email': 'testuser@example.com',
        'password': 'testpassword'
    }
    response = client.post(register_url, data=data)

    assert response.status_code == status.HTTP_201_CREATED
    assert User.objects.count() == 1
    assert User.objects.get(username='testuser')
