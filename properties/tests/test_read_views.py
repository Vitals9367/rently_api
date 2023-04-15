from pytest import mark
from django.urls import reverse
from rest_framework import status
from properties.models import Property
from properties.serializers import PropertySerializer
from .utils import get_test_resource

test_properties = get_test_resource('properties')


@mark.django_db
def test_get_properties(client, test_user):
    url = reverse('properties-list')

    # No properties first
    response = client.get(url)
    assert response.data == []
    assert response.status_code == status.HTTP_200_OK

    # Create some properties
    properties = [Property.objects.create(**prop, owner=test_user) for prop in test_properties]
    serializer = PropertySerializer(properties, many=True)

    # Newly created properties returned
    response = client.get(url)
    assert response.data == serializer.data
    assert response.status_code == status.HTTP_200_OK


@mark.django_db
def test_get_property_details(client, test_user):
    property_data = test_properties[0].copy()
    property_data['owner'] = test_user
    property = Property.objects.create(**property_data)

    url = reverse('properties-detail', kwargs={'pk': 'some-random-idasdasdasdasdasd'})

    response = client.get(url)

    # No details first
    assert response.data == {"detail": "Not found."}
    assert response.status_code == status.HTTP_404_NOT_FOUND

    # Get property details
    url = reverse('properties-detail', kwargs={'pk': str(property.id)})
    response = client.get(url)

    # Newly created property returned
    assert response.data == PropertySerializer(property).data
    assert response.status_code == status.HTTP_200_OK
