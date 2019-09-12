from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import (
    ModelSerializer
)

from campaigns.models import CampaignPartyRelation
from csecourses.models import CSECourseGroup
from qualification.models import Qualification, QuestionType, QualificationForm, QA


class GraderQualifiactionPublicResult(ModelSerializer):
    course = SerializerMethodField()
    scores = SerializerMethodField()
    participant_count = SerializerMethodField()

    class Meta:
        model = CampaignPartyRelation
        fields = [
            'course',
            'scores',
            'participant_count'
        ]

    def get_course(self, obj):

        if CSECourseGroup.objects.filter(
            course=obj.campaign.course_data.course_group.course
        ).count() > 1:
            return obj.campaign.course_data.course_group.course.title + ' گروه ' + str(obj.campaign.course_data.course_group.group)
        return obj.campaign.course_data.course_group.course.title + ' ' + obj.campaign.course_data.term.title

    def get_scores(self, obj):
        scores = []
        if not QA.objects.filter(
                qualification__dst=obj
        ).exists():
            return []

        # Hard coded here. probably a problem in design
        qform = QualificationForm.objects.first()  # TODO: Fix it

        for qfr in qform.questions.filter(question__type=QuestionType.TYPE_NUMBER):
            ans_qs = QA.objects.filter(
                question=qfr,
                qualification__dst=obj
            )
            if ans_qs.exists():
                ans_num = sum(
                        [
                            int(ans.answer) for ans in ans_qs
                        ]
                    ) // ans_qs.count()
            else:
                ans_num = 0
            scores.append(
                {
                    'question': qfr.question.result_body,
                    'answer': ans_num,
                    'count': ans_qs.count(),
                    'coeff': qfr.question.coeff
                }
            )
        return scores

    def get_participant_count(self, obj):
        return Qualification.objects.filter(dst=obj).count()