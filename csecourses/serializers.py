from django.contrib.auth import get_user_model
from enumfields.drf.serializers import EnumSupportSerializerMixin
from rest_framework.serializers import (
    ModelSerializer
)

from csecourses.models import CSECourse, CSECourseGroup, CSETerm, CSECourseGroupTerm

User = get_user_model()


class CSECourseSerializer(EnumSupportSerializerMixin, ModelSerializer):
    class Meta:
        model = CSECourse
        fields = [
            'cse_id',
            'title'
        ]


class CSECourseGroupSerializer(EnumSupportSerializerMixin, ModelSerializer):
    course = CSECourseSerializer()

    class Meta:
        model = CSECourseGroup
        fields = [
            'course',
            'group'
        ]


class CSETermSerializer(EnumSupportSerializerMixin, ModelSerializer):
    class Meta:
        model = CSETerm
        fields = [
            'title',
            'start',
            'end'
        ]


class CSECourseGroupTermSerializer(EnumSupportSerializerMixin, ModelSerializer):
    course_group = CSECourseGroupSerializer()
    term = CSETermSerializer()

    class Meta:
        model = CSECourseGroupTerm
        fields = [
            'course_group',
            'term',
        ]
