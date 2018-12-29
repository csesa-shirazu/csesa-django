from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils import timezone
from enumfields import Enum  # Uses Ethan Furman's "enum34" backport
from enumfields import EnumField
from sorl.thumbnail import ImageField


def campaign_image_upload_location(instance, filename):
    x = timezone.now()
    return "%s/%s/%s/%s" % (x.year, x.month, x.day, filename)


class CampaignType(Enum):
    COURSE = "course"
    WORKSHOP = "workshop"
    PRESENTATION = "presentation"
    EVENT = "event"


class Campaign(models.Model):
    course_data = models.ForeignKey(to="csecourses.CSECourseGroupTerm",
                                    on_delete=models.CASCADE,
                                    blank=True,
                                    null=True)

    title = models.CharField(max_length=10000, blank=True, null=True)

    type = EnumField(CampaignType, max_length=1000)

    slug = models.SlugField(blank=True, null=True)

    image = ImageField(upload_to=campaign_image_upload_location,
                       null=True,
                       blank=True,
                       width_field="width_field",
                       height_field="height_field")

    banner_image = models.ImageField(upload_to=campaign_image_upload_location,
                                     null=True,
                                     blank=True,
                                     width_field="banner_width_field",
                                     height_field="banner_height_field")

    width_field = models.IntegerField(default=0)
    height_field = models.IntegerField(default=0)
    banner_width_field = models.IntegerField(default=0)
    banner_height_field = models.IntegerField(default=0)

    description = models.TextField(blank=True, null=True)

    duration_days = models.IntegerField(blank=True, null=True)



    @property
    def name(self):
        if self.title:
            return self.title
        elif self.course_data:
            return str(self.course_data)
        return ""

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ("slug", "type")


class CampaignPartyRelationType(Enum):  # A subclass of Enum
    CREATOR = "creator"
    STUDENT = "student"
    TEACHER = "teacher"
    GRADER = "grader"
    MANAGER = "manager"
    MEMBER = "member"


class CampaignPartyRelation(models.Model):
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)

    # party
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    type = EnumField(CampaignPartyRelationType, max_length=1000)

    def __str__(self):
        return str(self.content_object) + " | " + self.campaign.title