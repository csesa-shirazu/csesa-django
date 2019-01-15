from django.db.models import Q
from rest_framework.generics import (
    ListAPIView
)
from rest_framework.permissions import (
    AllowAny,
)

from campaigns.models import CampaignPartyRelation
from qualification.models import Qualification
from .serializers import (
    GraderQualifiactionResult
)

from users.models import User

class QualifiactionResultAPIView(ListAPIView):
    serializer_class = GraderQualifiactionResult
    permission_classes = [AllowAny]
    lookup_field = ['slug']

    def get_queryset(self, *args, **kwargs):
        print(kwargs)
        print(args)
        print(self.kwargs['username'])
        profile = User.objects.get(username=self.kwargs['username']).profile.first()

        queryset_list = Qualification.objects.filter(
            dst__in=CampaignPartyRelation.objects.filter(
                campaign_relations_profiles=profile
            )
        )

        return queryset_list














