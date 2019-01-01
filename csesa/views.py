from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse

from campaigns.models import CampaignPartyRelation, CampaignPartyRelationType
from campaigns.serializers import GraderRelationSerializer


def index_view(request):
    if request.user.is_authenticated:
        return redirect(reverse('qualification:form', kwargs={'slug': 'cse-gradery'}))
    else:
        return redirect(reverse('users:login') + "?next=" + reverse('qualification:form', kwargs={'slug': 'cse-gradery'}))



def graders_view(request):
    if request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser):
        context = {
            'gcrs': GraderRelationSerializer(
                CampaignPartyRelation.objects.filter(
                    type = CampaignPartyRelationType.GRADER
                ), many=True
            ).data
        }
        return render(request, "graders.html", context)
    raise Http404

