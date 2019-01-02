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
    coeff = SerializerMethodField()
    body = SerializerMethodField()
    type = SerializerMethodField()

    class Meta:
        model = QuestionQualificationRelation
        fields = [
            'id',
            'coeff',
            'body',
            'type',
            'place'
        ]

    def get_coeff(self, obj):
        return obj.question.coeff

    def get_body(self, obj):
        return obj.question.body

    def get_type(self, obj):
        return QuestionSerializer(
            obj.question
        ).data['type']


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
