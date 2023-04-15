from pytest import mark
from django.urls import reverse
from rest_framework import status
from properties.models import Property
from properties.serializers import PropertySerializer
from .utils import get_test_resource


test_properties = get_test_resource('properties')


@mark.django_db
def test_post_property(client, authenticated_user):
    url = reverse('property-list')
    user, jwt_token = authenticated_user

    response = client.get(url)

    # No properties first
    assert response.data == []
    assert response.status_code == status.HTTP_200_OK

    # Create property with random jwt token
    client.credentials(HTTP_AUTHORIZATION='Bearer some-random-token-54as4dasd6asd')
    response = client.post(url, test_properties[0])
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # Create property with proper jwt token
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {jwt_token}')
    response = client.post(url, test_properties[0])

    # Newly created property returned
    assert response.data['title'] == test_properties[0]['title']
    assert response.data['description'] == test_properties[0]['description']
    assert response.data['rent'] == test_properties[0]['rent']
    assert response.status_code == status.HTTP_201_CREATED


@mark.django_db
def test_delete_property(client, authenticated_user):
    user, jwt_token = authenticated_user

    property = Property.objects.create(**test_properties[0], owner=user)
    serializer = PropertySerializer(property)

    url = reverse('property-detail-view', kwargs={'id': property.id})

    response = client.get(url)

    # Property exists
    assert response.data == serializer.data
    assert response.status_code == status.HTTP_200_OK

    # Try to delete without JWT token
    client.credentials(HTTP_AUTHORIZATION='Bearer some-random-token-54as4dasd6asd')
    response = client.delete(url)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # Try to delete with JWT token
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {jwt_token}')
    response = client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT

    # Property not found
    response = client.get(url)
    assert response.data == {"detail": "Not found."}
    assert response.status_code == status.HTTP_404_NOT_FOUND


@mark.django_db
def test_update_property(client, authenticated_user):
    user, jwt_token = authenticated_user

    property = Property.objects.create(**test_properties[0], owner=user)
    serializer = PropertySerializer(property)

    url = reverse('property-detail-view', kwargs={'id': property.id})
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
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {jwt_token}')
    response = client.put(url, {**test_properties[0], **updated_data})

    # Checks if data was updated
    assert response.data == {**serializer.data, **updated_data, 'updated_at': response.data['updated_at']}
    # Checks if updated_at timestamp is different
    assert serializer.data['updated_at'] != response.data['updated_at']
    assert response.status_code == status.HTTP_200_OK
