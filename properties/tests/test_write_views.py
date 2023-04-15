from pytest import mark
from django.urls import reverse
from rest_framework import status
from properties.models import Property
from properties.serializers import PropertySerializer
from .utils import get_test_resource

test_properties = get_test_resource('properties')


@mark.django_db
def test_create_property(client, authenticated_test_user):
    user, access_token, refresh_token = authenticated_test_user
    url = reverse('properties-list')
    auth_header = {'HTTP_AUTHORIZATION': f'Bearer {access_token}'}

    def assert_property_response(response, expected_data, expected_status):
        assert response.data['title'] == expected_data['title']
        assert response.data['description'] == expected_data['description']
        assert response.data['rent'] == expected_data['rent']
        assert response.status_code == expected_status

    def create_property(auth_header, data):
        client.credentials(**auth_header)
        return client.post(url, data)

    # Verify that no properties exist initially
    response = client.get(url)
    assert response.data == []
    assert response.status_code == status.HTTP_200_OK

    # Create a property with invalid token
    response = create_property({'HTTP_AUTHORIZATION': 'Bearer some-random-token-54as4dasd6asd'}, test_properties[0])
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # Create a property with valid token
    response = create_property(auth_header, test_properties[0])
    assert_property_response(response, test_properties[0], status.HTTP_201_CREATED)


@mark.django_db
def test_delete_property(client, authenticated_test_user):
    user, access_token, refresh_token = authenticated_test_user

    property = Property.objects.create(**test_properties[0], owner=user)
    serializer = PropertySerializer(property)

    url = reverse('properties-detail', kwargs={'pk': str(property.id)})

    # Assert that the property exists
    response = client.get(url)
    assert response.data == serializer.data
    assert response.status_code == status.HTTP_200_OK

    # Try to delete without JWT token
    client.credentials(HTTP_AUTHORIZATION='Bearer some-random-token-54as4dasd6asd')
    response = client.delete(url)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # Delete with JWT token
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
    response = client.delete(url)

    # Assert that the property is deleted
    assert response.status_code == status.HTTP_204_NO_CONTENT

    # Assert that the property is not found
    response = client.get(url)
    assert response.data == {"detail": "Not found."}
    assert response.status_code == status.HTTP_404_NOT_FOUND


@mark.django_db
def test_update_property(client, authenticated_test_user):
    user, access_token, refresh_token = authenticated_test_user

    property = Property.objects.create(**test_properties[0], owner=user)
    serializer = PropertySerializer(property)

    url = reverse('properties-detail', kwargs={'pk': str(property.id)})
    response = client.get(url)

    # Property exists
    assert response.data == serializer.data
    assert response.status_code == status.HTTP_200_OK

    updated_data = {
        'title': "new title of property",
        'rooms': 20,
        'rent': '678.15',
        'sq_m': 2456,
        'address': 'asdasdasda5s56da65ads65ads65'
    }

    # Try to update without JWT token
    client.credentials(HTTP_AUTHORIZATION='Bearer some-random-token-54as4dasd6asd')
    response = client.put(url, {**test_properties[0], **updated_data})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # Try with JWT token
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
    response = client.put(url, {**test_properties[0], **updated_data})

    # Checks if data was updated
    updated_property = Property.objects.get(id=property.id)
    assert response.data == PropertySerializer(updated_property).data
    assert response.status_code == status.HTTP_200_OK
