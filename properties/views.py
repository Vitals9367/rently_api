from django.core.exceptions import PermissionDenied
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from rest_framework import generics, permissions
from properties.models import Property
from properties.serializers import PropertySerializer


class PropertyView(generics.ListCreateAPIView):
    serializer_class = PropertySerializer
    permission_classes = [permissions.AllowAny]
    authentication_classes = [JWTAuthentication]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['owner', 'city', 'state', 'rooms']
    ordering_fields = ['rent']
    queryset = Property.objects.all()

    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            serializer.save(owner=self.request.user)
        else:
            raise PermissionDenied('You must be authenticated to access this resource')


def get_owned_property(self_object):
    '''
    Returns property object if it's owned by the user requesting it
    '''
    if not self_object.request.user.is_authenticated:
        raise PermissionDenied('You must be authenticated to perform delete')

    property = self_object.get_object()

    if self_object.request.user != property.owner:
        raise PermissionDenied('You must be owner to perform delete')

    return property


def perform_update(self_object, request, partial_update=False):
    '''
    Performs PUT / PATCH update based on partial_update variable
    '''
    property = get_owned_property(self_object)

    serializer = self_object.get_serializer(property, data=request.data, partial=partial_update)
    serializer.is_valid(raise_exception=True)
    self_object.perform_update(serializer)
    return serializer.data


class PropertyDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PropertySerializer
    lookup_url_kwarg = 'id'
    queryset = Property.objects.all()
    authentication_classes = [JWTAuthentication]

    def destroy(self, request, *args, **kwargs):
        property = get_owned_property(self)

        self.perform_destroy(property)
        return Response(status=204)

    def update(self, request, *args, **kwargs):
        updated_property = perform_update(self, request, partial_update=False)
        return Response(updated_property, status=200)

    def partial_update(self, request, *args, **kwargs):
        updated_property = perform_update(self, request, partial_update=True)
        return Response(updated_property, status=200)
