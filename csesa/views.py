from django.shortcuts import render, redirect
from django.urls import reverse

from campaigns.models import Campaign, CampaignType, BidAcceptedRange
from campaigns.serializers import ProjectListSerializer, BidAcceptedRangeSerializer
from noorando.utils.contexts import get_dashboard_context
from taxonomy.models import Term, Taxonomy, TaxonomyType
from taxonomy.serializers import TermSerializer
from users.serializers import ProfileRetrieveSerializer


def index_view(request):
    context = {
        "projects": ProjectListSerializer(
            Campaign.objects.filter(type=CampaignType.PROJECT),
            many=True
        ).data,
        "bid_ranges": BidAcceptedRangeSerializer(
            BidAcceptedRange.objects.all(),
            many=True
        ).data,
        'skills': TermSerializer(
            Term.objects.filter(
                taxonomies=Taxonomy.objects.get(title=TaxonomyType.SKILL) # if taxonomy type we want is in taxonomies
            ),
            many=True
        ).data,
        'project_categories': TermSerializer(
            Term.objects.filter(
                taxonomies=Taxonomy.objects.get(title=TaxonomyType.PROJECT_CATEGORY) # if taxonomy type we want is in taxonomies
            ),
            many=True
        ).data
    }
    return render(request, "index.html", context)



def dashboard_view(request):
    if request.user.is_authenticated:
        context = get_dashboard_context(request)
        return render(request, "dashboard.html", context)
    else:
        return redirect(reverse('users:login') + "?next=" + request.path_info)

