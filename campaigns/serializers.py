from django.contrib.auth import get_user_model
from enumfields.drf.serializers import EnumSupportSerializerMixin
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import (
    ModelSerializer
)

from campaigns.models import Campaign, CampaignPartyRelation
from csecourses.serializers import CSECourseGroupTermSerializer
from users.serializers import ProfileRetrieveSerializer

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


class CampaignAsCourseSimpleSerializer(EnumSupportSerializerMixin, ModelSerializer):
    title = SerializerMethodField()
    group = SerializerMethodField()

    class Meta:
        model = Campaign
        fields = [
            'id',
            'title',
            'group',
        ]

    def get_title(self, obj: Campaign):
        return obj.course_data.course_group.course.title

    def get_group(self, obj: Campaign):
        return obj.course_data.course_group.group


class GraderRelationSerializer(EnumSupportSerializerMixin, ModelSerializer):
    campaign = CampaignAsCourseSimpleSerializer()
    content_object = ProfileRetrieveSerializer()
    class Meta:
        model = CampaignPartyRelation
        fields = [
            'campaign',
            'content_object'
        ]
