from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils import timezone
from enumfields import Enum  # Uses Ethan Furman's "enum34" backport
from enumfields import EnumField
from sorl.thumbnail import ImageField

from users.models import Profile
from users.serializers import ProfileRetrieveSerializer


def campaign_image_upload_location(instance, filename):
    x = timezone.now()
    return "%s/%s/%s/%s" % (x.year, x.month, x.day, filename)


class CampaignType(Enum):
    COURSE = "course"
    WORKSHOP = "workshop"
    PRESENTATION = "presentation"
    EVENT = "event"


class Campaign(models.Model):
    """
        Part of my own design pattern. For describing any works
        and acts done by people. for example, A specific course
        in a specific term that has a teacher, some graders and
        some students
    """
    course_data = models.ForeignKey(to="csecourses.CSECourseGroupTerm",
                                    on_delete=models.CASCADE,
                                    blank=True,
                                    null=True)

    type = EnumField(CampaignType, max_length=1000)

    @property
    def students(self):
        return ProfileRetrieveSerializer(
            Profile.objects.filter(campaign_relations__in=CampaignPartyRelation.objects.filter(
                campaign=self,
                content_type=ContentType.objects.get(model='profile'),
                type=CampaignPartyRelationType.STUDENT
            ).all()), many=True).data

    @property
    def graders(self):
        return ProfileRetrieveSerializer(
            Profile.objects.filter(campaign_relations__in=CampaignPartyRelation.objects.filter(
                campaign=self,
                content_type=ContentType.objects.get(model='profile'),
                type=CampaignPartyRelationType.GRADER
            ).all()).order_by('-id'), many=True).data

    @property
    def name(self):
        if self.title:
            return self.title
        elif self.course_data:
            return str(self.course_data)
        return ""

    def __str__(self):
        return self.name


class CampaignPartyRelationType(Enum):  # A subclass of Enum
    CREATOR = "creator"
    STUDENT = "student"
    TEACHER = "teacher"
    GRADER = "grader"
    MANAGER = "manager"
    MEMBER = "member"

class CampaignPartyRelationStatus(Enum):  # A subclass of Enum
    APPROVED = "approved"
    PENDING = "pending"
    REJECTED = "rejected"


class CampaignPartyRelation(models.Model):
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name='cprelations')

    enrollment_request_note = models.TextField(blank=True, null=True)

    # party
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    type = EnumField(CampaignPartyRelationType, max_length=1000)
    status = EnumField(CampaignPartyRelationStatus, max_length=1000)

    def __str__(self):
        return str(self.content_object) + " | " + str(self.campaign)