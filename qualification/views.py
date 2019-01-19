from django.contrib.contenttypes.models import ContentType
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import View

from campaigns.models import Campaign, CampaignPartyRelation, CampaignPartyRelationType
from campaigns.serializers import CampaignAsCourseSerializer
from qualification.models import QualificationForm, Qualification, QA
from qualification.serializers import QualificationFormSerializer
from users.models import Profile


class qualification_view(View):
    template_name = 'grader-qualification.html'

    @staticmethod
    def the_context(request, the_form):
        the_profile = request.user.profile.first()
        context = {
            'courses': CampaignAsCourseSerializer(
                Campaign.objects.filter(
                    cprelations__in=CampaignPartyRelation.objects.filter(
                        object_id=the_profile.id,
                        type=CampaignPartyRelationType.STUDENT
                    )
                ),
                many=True
            ).data,
            'the_form': QualificationFormSerializer(
                the_form,
            ).data
        }
        the_student = request.user.profile.first()
        for course in context['courses']:
            for grader in course['graders']:
                the_campaign = get_object_or_404(Campaign, id=int(course['id']))
                the_grader = get_object_or_404(Profile, id=int(grader['id']))
                the_grader_cpr = CampaignPartyRelation.objects.get(
                    type=CampaignPartyRelationType.GRADER,
                    content_type=ContentType.objects.get_for_model(the_grader),
                    object_id=the_grader.id,
                    campaign=the_campaign
                )
                the_student_cpr = CampaignPartyRelation.objects.get(
                    type=CampaignPartyRelationType.STUDENT,
                    content_type=ContentType.objects.get_for_model(the_student),
                    object_id=the_student.id,
                    campaign=the_campaign
                )

                if Qualification.objects.filter(
                    src=the_student_cpr,
                    dst=the_grader_cpr
                ).exists():
                    grader['done'] = 'true'
                else:
                    grader['done'] = 'false'

        return context

    def get(self, request, slug=None, *args, **kwargs):
        the_form = get_object_or_404(QualificationForm, slug=slug)
        if request.user.is_authenticated:
            context = self.the_context(request, the_form)
            return render(request, self.template_name, context)
        else:
            return redirect(reverse('users:login') + "?next=" + request.path_info)

    @transaction.atomic
    def post(self, request, slug=None, *args, **kwargs):
        the_form = get_object_or_404(QualificationForm, slug=slug)
        if request.user.is_authenticated:
            context = {}

            the_student = request.user.profile.first()
            the_campaign = get_object_or_404(Campaign, id=int(request.POST['course_id']))
            the_grader = get_object_or_404(Profile, id=int(request.POST['grader_id']))
            the_grader_cpr = CampaignPartyRelation.objects.get(
                type=CampaignPartyRelationType.GRADER,
                content_type=ContentType.objects.get_for_model(the_grader),
                object_id=the_grader.id,
                campaign=the_campaign
            )
            the_student_cpr = CampaignPartyRelation.objects.get(
                type=CampaignPartyRelationType.STUDENT,
                content_type=ContentType.objects.get_for_model(the_student),
                object_id=the_student.id,
                campaign=the_campaign
            )
            try:
                the_qualification = Qualification.objects.get(
                    src=the_student_cpr,
                    dst=the_grader_cpr
                )
                edit = True
            except:
                the_qualification = Qualification.objects.create(
                    src=the_student_cpr,
                    dst=the_grader_cpr
                )
                edit = False
            for qr in the_form.questions.all():
                if 'ans_' + str(qr.id) in request.POST and qr.question.is_valid_ans(request.POST['ans_' + str(qr.id)]):

                    the_qa_qs = QA.objects.filter(
                            qualification=the_qualification,
                            question=qr
                        )

                    if the_qa_qs.exists():
                        the_qa = the_qa_qs.first()
                        if request.POST['ans_' + str(qr.id)] != '-1':
                            the_qa.answer = request.POST['ans_' + str(qr.id)]
                            the_qa.save()
                        else:
                            the_qa.delete()

                    else:
                        if request.POST['ans_' + str(qr.id)] != '-1':
                            QA.objects.create(
                                qualification=the_qualification,
                                question=qr,
                                answer=request.POST['ans_' + str(qr.id)],
                            )
                else:
                    context['status'] = 'error'
                    if not edit:
                        the_qualification.delete()
                        break

            if 'status' not in context:
                if edit:
                    context['status'] = 'modified'
                else:
                    context['status'] = 'new'

            context.update(self.the_context(request, the_form))
            return render(request, self.template_name, context)
        else:
            return redirect(reverse('users:login') + "?next=" + request.path_info)

# Create your views here.
class result_view(View):
    template_name = 'grader-qualification-result.html'

    def get(self, request, slug=None, *args, **kwargs):
        context = {
            'slug': slug
        }
        return render(request, self.template_name, context)
