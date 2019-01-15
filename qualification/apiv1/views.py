from django.db.models import Q
from rest_framework.generics import (
    ListAPIView
)
from rest_framework.permissions import (
    AllowAny,
)

from campaigns.models import CampaignPartyRelation, CampaignPartyRelationType
from qualification.models import Qualification
from .serializers import (
    GraderQualifiactionPublicResult
)

from users.models import User


class QualifiactionResultAPIView(ListAPIView):
    serializer_class = GraderQualifiactionPublicResult
    permission_classes = [AllowAny]
    lookup_field = ['slug']

    def get_queryset(self, *args, **kwargs):
        profile = User.objects.get(username=self.kwargs['username']).profile.first()

        queryset_list = CampaignPartyRelation.objects.filter(
            campaign_relations_profiles=profile,
            type=CampaignPartyRelationType.GRADER
        )

        return queryset_list
