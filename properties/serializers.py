from rest_framework import serializers
from properties.models import Property


class PropertySerializer(serializers.ModelSerializer):

    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Property
        fields = '__all__'
