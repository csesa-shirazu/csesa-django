from django.contrib.auth import get_user_model
from enumfields.drf.serializers import EnumSupportSerializerMixin
from rest_framework.serializers import (
    ModelSerializer
)

from qualification.models import QualificationForm, Question

User = get_user_model()


class QualificationQuestionSerializer(EnumSupportSerializerMixin, ModelSerializer):
    class Meta:
        model = Question
        fields = [
            'id',
            'coeff',
            'body',
            'type'
        ]


class QualificationFormSerializer(EnumSupportSerializerMixin, ModelSerializer):
    questions = QualificationQuestionSerializer(many=True)

    class Meta:
        model = QualificationForm
        fields = [
            'id',
            'slug',
            'questions'
        ]
