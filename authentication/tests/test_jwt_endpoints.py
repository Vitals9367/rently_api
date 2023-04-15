import pytest
from django.urls import reverse
from rest_framework import status

TOKEN_OBTAIN_URL = reverse('token-obtain')
TOKEN_VERIFY_URL = reverse('token-verify')
TOKEN_REFRESH_URL = reverse('token-refresh')
TOKEN_BLACKLIST_URL = reverse('token-blacklist')


def assert_post_request(client, url, payload, status_code=status.HTTP_200_OK):
    response = client.post(url, payload)
    assert response.status_code == status_code
    return response


def assert_token_refresh(client, token, status_code=status.HTTP_200_OK):
    response = assert_post_request(client, TOKEN_REFRESH_URL, {"refresh": str(token)}, status_code)
    if status_code == status.HTTP_200_OK:
        assert 'access' in response.data
    return response


def verify_token(client, token, status_code=status.HTTP_200_OK):
    return assert_post_request(client, TOKEN_VERIFY_URL, {"token": str(token)}, status_code)


@pytest.mark.parametrize("method", ["get", "put", "patch", "delete"])
@pytest.mark.parametrize("endpoint", [TOKEN_OBTAIN_URL, TOKEN_REFRESH_URL, TOKEN_BLACKLIST_URL, TOKEN_VERIFY_URL])
def test_not_allowed_methods(client, method, endpoint):
    assert (getattr(client, method)(endpoint, format="json").status_code == status.HTTP_405_METHOD_NOT_ALLOWED)


@pytest.mark.django_db
def test_refresh_token(client, authenticated_test_user):
    user, access_token, refresh_token = authenticated_test_user

    response = assert_post_request(client, TOKEN_REFRESH_URL, {"refresh": ""}, status.HTTP_400_BAD_REQUEST)

    # Don't allow empty inputs
    assert response.data == {"refresh": ["This field may not be blank."]}

    response = assert_token_refresh(client, refresh_token)

    # Tokens are valid
    verify_token(client, response.data['access'])


@pytest.mark.django_db
def test_blacklist_token(client, authenticated_test_user):
    user, access_token, refresh_token = authenticated_test_user

    response = assert_post_request(client, TOKEN_BLACKLIST_URL, {"refresh": ""}, status.HTTP_400_BAD_REQUEST)

    # Don't allow empty inputs
    assert response.data == {"refresh": ["This field may not be blank."]}

    response = assert_post_request(client, TOKEN_BLACKLIST_URL, {"refresh": str(refresh_token)}, status.HTTP_200_OK)

    # Response contains token
    assert response.status_code == status.HTTP_200_OK

    # Tokens are not valid anymore
    assert_token_refresh(client, refresh_token, status.HTTP_401_UNAUTHORIZED)


@pytest.mark.django_db
def test_obtain_token(client, test_user):
    response = assert_post_request(client, TOKEN_OBTAIN_URL, {"username": "", "password": ""}, status.HTTP_400_BAD_REQUEST)

    # Don't allow empty inputs
    assert response.data == {"username": ["This field may not be blank."], "password": ["This field may not be blank."]}

    response = assert_post_request(client, TOKEN_OBTAIN_URL, {"username": test_user.username, "password": test_user.password}, status.HTTP_200_OK)

    # Response contains tokens
    assert 'refresh' in response.data
    assert 'access' in response.data

    # Tokens are valid
    verify_token(client, response.data['access'])
    verify_token(client, response.data['refresh'])
