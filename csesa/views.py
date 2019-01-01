from django.contrib.contenttypes.models import ContentType
from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse

from campaigns.models import CampaignPartyRelation, CampaignPartyRelationType, Campaign
from campaigns.serializers import GraderRelationSerializer, CampaignAsCourseSimpleSerializer
from users.models import User, Profile


def index_view(request):
    if request.user.is_authenticated:
        return redirect(reverse('qualification:form', kwargs={'slug': 'cse-gradery'}))
    else:
        return redirect(reverse('users:login') + "?next=" + reverse('qualification:form', kwargs={'slug': 'cse-gradery'}))



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
                        campaign = the_campaign,
                        content_type = ContentType.objects.get_for_model(the_grader),
                        object_id = the_grader.id,
                        type=CampaignPartyRelationType.GRADER
                    ).exists():
                        context['message'] = 'گریدر از قبل وارد شده'
                    else:
                        CampaignPartyRelation.objects.create(
                            campaign = the_campaign,
                            content_type = ContentType.objects.get_for_model(the_grader),
                            object_id = the_grader.id,
                            type=CampaignPartyRelationType.GRADER
                        )
                        context['message'] = 'با موفقیت ثبت شد'

        context.update({
            'gcrs': GraderRelationSerializer(
                CampaignPartyRelation.objects.filter(
                    type = CampaignPartyRelationType.GRADER
                ), many=True
            ).data,
            'courses': CampaignAsCourseSimpleSerializer(
                Campaign.objects.all(),
                many=True
            ).data
        })
        return render(request, "graders.html", context)
    raise Http404

