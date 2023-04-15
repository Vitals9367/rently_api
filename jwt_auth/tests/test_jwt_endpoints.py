import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User

url_obtain = reverse('token_obtain')
url_verify = reverse('token_verify')
url_refresh = reverse('token_refresh')
url_blacklist = reverse('token_blacklist')


def perform_token_refresh(token, client, status_code=status.HTTP_200_OK):
    refresh_response = client.post(url_refresh, {
        "refresh": str(token)
    })

    assert refresh_response.status_code == status_code
    return refresh_response


def verify_token(token, client, status_code=status.HTTP_200_OK):
    verify_response = client.post(url_verify, {
        "token": str(token)
    })

    assert verify_response.status_code == status_code
    return verify_response


@pytest.fixture
def obtain_tokens():
    user = User.objects.create_user(
        username='testuser', password='testpassword'
    )
    refresh_token = RefreshToken.for_user(user)

    return refresh_token.access_token, refresh_token


@pytest.mark.parametrize("method", ["get", "put", "patch", "delete"])
@pytest.mark.parametrize("endpoint", ["token_obtain", "token_refresh", "token_blacklist", "token_verify"])
def test_not_allowed_methods(client, method, endpoint):
    assert (getattr(client, method)(reverse(endpoint), format="json").status_code == 405)


@pytest.mark.django_db
def test_refresh_token(client, obtain_tokens):
    access_token, refresh_token = obtain_tokens

    response = client.post(url_refresh, {
        "refresh": "",
    })

    # Don't allow empty inputs
    assert response.data == {"refresh": ["This field may not be blank."]}
    assert response.status_code == status.HTTP_400_BAD_REQUEST

    response = perform_token_refresh(refresh_token, client)

    # Response contains token
    assert 'access' in response.data

    # Tokens are valid
    verify_token(response.data['access'], client)


@pytest.mark.django_db
def test_blacklist_token(client, obtain_tokens):
    access_token, refresh_token = obtain_tokens

    response = client.post(url_blacklist, {
        "refresh": "",
    })

    # Don't allow empty inputs
    assert response.data == {"refresh": ["This field may not be blank."]}
    assert response.status_code == status.HTTP_400_BAD_REQUEST

    response = client.post(url_blacklist, {
        "refresh": str(refresh_token),
    })

    # Response contains token
    assert response.status_code == status.HTTP_200_OK

    # Tokens are not valid anymore
    perform_token_refresh(refresh_token, client, status.HTTP_401_UNAUTHORIZED)


@pytest.mark.django_db
def test_obtain_token(client, user):
    response = client.post(url_obtain, {
        "username": "",
        "password": ""
    })

    # Don't allow empty inputs
    assert response.data == {"username": ["This field may not be blank."], "password": ["This field may not be blank."]}
    assert response.status_code == status.HTTP_400_BAD_REQUEST

    response = client.post(url_obtain, {
        "username": "testuser",
        "password": "testpass"
    })

    # Response contains tokens
    assert 'refresh' in response.data
    assert 'access' in response.data
    assert response.status_code == status.HTTP_200_OK

    # Tokens are valid
    verify_token(response.data['access'], client)
    verify_token(response.data['refresh'], client)
