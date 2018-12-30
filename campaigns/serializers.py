from django.contrib.auth import get_user_model
from enumfields.drf.serializers import EnumSupportSerializerMixin
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import (
    ModelSerializer
)

from campaigns.models import Campaign
from csecourses.serializers import CSECourseGroupTermSerializer

User = get_user_model()


class CampaignAsCourseSerializer(EnumSupportSerializerMixin, ModelSerializer):
    title = SerializerMethodField()

    class Meta:
        model = Campaign
        fields = [
            'id',
            'title',
            'graders'
        ]

    def get_title(self, obj: Campaign):
        return obj.course_data.course_group.course.title
