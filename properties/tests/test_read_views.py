from pytest import mark
from django.urls import reverse
from rest_framework import status
from properties.models import Property
from properties.serializers import PropertySerializer
from .utils import get_test_resource

test_properties = get_test_resource('properties')


@mark.django_db
def test_get_properties(client, user):
    url = reverse('property-list')

    response = client.get(url)

    # No properties first
    assert response.data == []
    assert response.status_code == status.HTTP_200_OK

    # Create some properties
    property1 = Property.objects.create(**test_properties[0], owner=user)
    property2 = Property.objects.create(**test_properties[1], owner=user)
    serializer = PropertySerializer([property1, property2], many=True)

    response = client.get(url)

    # Newly created properties returned
    assert response.data == serializer.data
    assert response.status_code == status.HTTP_200_OK


@mark.django_db
def test_get_properties_details(client, user):

    property = Property(**test_properties[0], owner=user)

    url = reverse('property-detail-view', kwargs={'id': property.id})

    response = client.get(url)

    # No details first
    assert response.data == {"detail": "Not found."}
    assert response.status_code == status.HTTP_404_NOT_FOUND

    # Create property
    property.save()
    serializer = PropertySerializer(property)

    response = client.get(url)

    # Newly created property returned
    assert response.data == serializer.data
    assert response.status_code == status.HTTP_200_OK
