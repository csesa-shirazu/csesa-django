from enumfields.drf import EnumSupportSerializerMixin
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from campaigns.models import CampaignPartyRelation, CampaignPartyRelationStatus
from csecourses.models import CSECourseGroup
from qualification.models import QA, QualificationForm, Qualification, QuestionType


class GraderOfCourseRelationSerializer(EnumSupportSerializerMixin, ModelSerializer):
    score = SerializerMethodField()
    grader_profile = SerializerMethodField()
    accessable = SerializerMethodField()
    enrollment_request_note = SerializerMethodField()

    class Meta:
        model = CampaignPartyRelation
        fields = [
            'id',
            'grader_profile',
            'status',
            'score',
            'enrollment_request_note',
            'accessable',
        ]


    def get_accessable(self, obj):
        if obj.status == CampaignPartyRelationStatus.APPROVED:
            return False
        user = self.context.get('request').user
        if user.is_authenticated and obj.content_object == user.profile.first():
            return True
        return False

    def get_enrollment_request_note(self, obj):
        user = self.context.get('request').user
        if (user.is_authenticated and obj.content_object == user.profile.first()) or self.context.get('is_teacher'):
            return obj.enrollment_request_note
        return None

    def get_grader_profile(self, obj):
        return {
            'id': obj.object_id,
            'first_name': obj.content_object.first_name,
            'last_name': obj.content_object.last_name,
        }

    def get_score(self, obj):
        if not QA.objects.filter(
                qualification__dst=obj
        ).exists():
            return 0

        # Hard coded here. probably a problem in design
        qform = QualificationForm.objects.first()  # TODO: Fix it

        ans_total = 0
        coeff_total = 0

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
                ans_total += ans_num * qfr.question.coeff
                coeff_total += qfr.question.coeff

        if coeff_total > 0:
            return (ans_total // coeff_total) + ((ans_total / coeff_total * 10) % 10 > 5)
        return 0

    def get_participant_count(self, obj):
        return Qualification.objects.filter(dst=obj).count()