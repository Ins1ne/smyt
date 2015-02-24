from rest_framework import serializers

from office.models import DynamicModel


# XXX We can create serializers dynamically too, but it's just example
class RoomSerializer(serializers.ModelSerializer):
    """Serializer for Room model."""

    class Meta:
        model = DynamicModel.get_model('room')


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model."""

    class Meta:
        model = DynamicModel.get_model('user')
