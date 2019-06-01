from enumfields.drf import EnumSupportSerializerMixin
from rest_framework.serializers import ModelSerializer

from campaigns.models import CampaignSubscription


class CampaignSubscriptionSerializer(EnumSupportSerializerMixin, ModelSerializer):
    class Meta:
        model = CampaignSubscription
        fields = [
            'id',
            'campaign',
            'email',
            'phone'
        ]