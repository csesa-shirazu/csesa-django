from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import (
    ModelSerializer
)

from qualification.models import Qualification


class GraderQualifiactionResult(ModelSerializer):
    course = SerializerMethodField()
    answers = SerializerMethodField()
    class Meta:
        model = Qualification
        fields = [
            'course',
            'answers'
        ]

    def get_course(self, obj):
        return obj.dst.course_data.course_group.course.title

    def get_answers(self, obj):
        answers = []
        return answers