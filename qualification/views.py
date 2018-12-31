from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import View
from rest_framework.renderers import JSONRenderer

from campaigns.models import Campaign, CampaignPartyRelation
from campaigns.serializers import CampaignAsCourseSerializer
from qualification.models import QualificationForm
from qualification.serializers import QualificationFormSerializer


class qualification_view(View):
    template_name = 'grader-qualification.html'

    @staticmethod
    def the_context(request, the_form):
        the_profile = request.user.profile.first()
        return {
                'courses': CampaignAsCourseSerializer(
                    Campaign.objects.filter(
                        cprelations__in = CampaignPartyRelation.objects.filter(
                            object_id=the_profile.id
                        )
                    ),
                    many=True
                ).data,
                'the_form': QualificationFormSerializer(
                    the_form,
                ).data
            }

    def get(self, request, slug=None, *args, **kwargs):
        the_form = get_object_or_404(QualificationForm, slug=slug)
        if request.user.is_authenticated:
            context = self.the_context(request, the_form)
            return render(request, self.template_name, context)
        else:
            return redirect(reverse('users:login') + "?next=" + request.path_info)

    def post(self, request, slug=None, *args, **kwargs):
        the_form = get_object_or_404(QualificationForm, slug=slug)
        if request.user.is_authenticated:

            # TODO: handle result here
            print(request.POST)
            context = self.the_context(request, the_form)
            return render(request, self.template_name, context)
        else:
            return redirect(reverse('users:login') + "?next=" + request.path_info)

# Create your views here.
