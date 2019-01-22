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

from users.models import User, Profile


class QualifiactionResultAPIView(ListAPIView):
    serializer_class = GraderQualifiactionPublicResult
    permission_classes = [AllowAny]
    lookup_field = ['slug']

    def get_queryset(self, *args, **kwargs):
        profile = Profile.objects.get(id=self.kwargs['profile_id'])

        queryset_list = CampaignPartyRelation.objects.filter(
            campaign_relations_profiles=profile,
            type=CampaignPartyRelationType.GRADER,
            dst_qualifications__isnull=False
        ).distinct()

        return queryset_list
