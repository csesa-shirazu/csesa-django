from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny

from campaigns.apiv1.serializers import CampaignSubscriptionSerializer
from campaigns.models import CampaignSubscription

from django_filters import rest_framework as filters


class CampaignSubscriptionCreateAPIView(CreateAPIView):
    serializer_class = CampaignSubscriptionSerializer
    permission_classes = [AllowAny]



class CampaignSubscriptionFilterClass(filters.FilterSet):
    class Meta:
        model = CampaignSubscription
        fields = {
            'campaign': ['exact'],
        }

class CampaignSubscriptionListAPIView(ListAPIView):
    serializer_class = CampaignSubscriptionSerializer
    permission_classes = [AllowAny]
    queryset = CampaignSubscription.objects.all()

    filter_class = CampaignSubscriptionFilterClass
    filter_backends = [filters.DjangoFilterBackend, SearchFilter]
    search_fields = ['campaign']