from django.contrib.contenttypes.models import ContentType
from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from campaigns.models import CampaignPartyRelation, CampaignPartyRelationType, Campaign
from campaigns.serializers import GraderRelationSerializer, CampaignAsCourseSimpleSerializer
from users.models import User, Profile
from users.serializers import ProfileRetrieveSerializer, ProfileRetrieveSimpleSerializer


def index_view(request):
    return redirect(reverse('qualification:result', kwargs={'slug': 'cse-gradery'}))
    # if request.user.is_authenticated:
    #     return redirect(reverse('qualification:form', kwargs={'slug': 'cse-gradery'}))
    # else:
    #     return redirect(
    #         reverse('users:login') + "?next=" + reverse('qualification:form', kwargs={'slug': 'cse-gradery'}))


def graders_view(request):
    if request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser):
        context = {}
        if 'gid' in request.POST:
            try:
                the_grader = User.objects.get(username=request.POST['gid']).profile.first()
            except User.DoesNotExist:
                context['message'] = 'پروفایل با این یوزرنیم وجود ندارد'
            else:
                try:
                    the_campaign = Campaign.objects.get(id=request.POST['cid'])
                except Campaign.DoesNotExist:
                    context['message'] = 'درس وارد شده نامعتبر است'
                else:
                    if CampaignPartyRelation.objects.filter(
                            campaign=the_campaign,
                            content_type=ContentType.objects.get_for_model(the_grader),
                            object_id=the_grader.id,
                            type=CampaignPartyRelationType.GRADER
                    ).exists():
                        context['message'] = 'گریدر از قبل وارد شده'
                    else:
                        CampaignPartyRelation.objects.create(
                            campaign=the_campaign,
                            content_type=ContentType.objects.get_for_model(the_grader),
                            object_id=the_grader.id,
                            type=CampaignPartyRelationType.GRADER
                        )
                        context['message'] = 'با موفقیت ثبت شد'

        context.update({
            'gcrs': GraderRelationSerializer(
                CampaignPartyRelation.objects.filter(
                    type=CampaignPartyRelationType.GRADER
                ), many=True
            ).data,
            'courses': CampaignAsCourseSimpleSerializer(
                Campaign.objects.all(),
                many=True
            ).data
        })
        return render(request, "graders.html", context)
    raise Http404


class GradersWithQualificationAPIView(APIView):
    authentication_class = []  # Don't forget to add a 'comma' after first element to make it a tuple

    permission_classes = [AllowAny]

    def get(self, request, format=None):
        data = ProfileRetrieveSimpleSerializer(
        Profile.objects.filter(campaign_relations__in=CampaignPartyRelation.objects.filter(
            content_type=ContentType.objects.get(model='profile'),
            type=CampaignPartyRelationType.GRADER,
            dst_qualifications__isnull=False
        ).all()).distinct().order_by('-id'), many=True).data

        return Response(data)
