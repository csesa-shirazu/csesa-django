from django.contrib.auth import get_user_model
from rest_framework.serializers import (
    ModelSerializer
)

from users.models import Profile

User = get_user_model()


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'first_name',
            'last_name',
            'email'
        ]


class ProfileRetrieveSerializer(ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Profile
        fields = [
            'id',
            'user',
            'campaign_relations'
        ]

class ProfileRetrieveSimpleSerializer(ModelSerializer):
    class Meta:
        model = Profile
        fields = [
            'id',
            'first_name',
            'last_name'
        ]
