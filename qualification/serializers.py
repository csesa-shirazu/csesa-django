from django.contrib.auth import get_user_model
from enumfields.drf.serializers import EnumSupportSerializerMixin
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import (
    ModelSerializer
)

from qualification.models import QualificationForm, Question, QuestionQualificationRelation

User = get_user_model()


class QuestionSerializer(EnumSupportSerializerMixin, ModelSerializer):
    class Meta:
        model = Question
        fields = [
            'id',
            'coeff',
            'body',
            'type',
        ]

class QualificationQuestionSerializer(EnumSupportSerializerMixin, ModelSerializer):
    question = QuestionSerializer()
    class Meta:
        model = QuestionQualificationRelation
        fields = [
            'id',
            'question',
            'place'
        ]


class QualificationFormSerializer(EnumSupportSerializerMixin, ModelSerializer):
    questions = SerializerMethodField()

    class Meta:
        model = QualificationForm
        fields = [
            'id',
            'slug',
            'questions'
        ]
    def get_questions(self, obj):
        return QualificationQuestionSerializer(
            obj.questions.all().order_by('place')
            ,many=True
        ).data
