from rest_framework import serializers

from connections.models import FriendRequest
from users.models import User
from users.serializers import UserSerializer


class FriendRequestListSerializer(serializers.ModelSerializer):
    """
    User model Serializer
    """
    friend = UserSerializer()

    class Meta:
        model = FriendRequest
        fields = ('friend', 'id')

