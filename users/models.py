from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.contrib.auth.models import User

# from campaigns.models import CampaignPartyRelation
from django.db.models.signals import post_save


def profile_image_upload_location(instance, filename):
    return "user/%s/profile/%s" % (instance.user.id, filename)


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="profile")

    name_prefix = models.CharField(blank=True, null=True, max_length=255)  # TODO: convert to enum or class
    first_name = models.CharField(blank=True, null=True, max_length=255)
    last_name = models.CharField(blank=True, null=True, max_length=255)

    profile_image = models.ImageField(upload_to=profile_image_upload_location,
                                      null=True,
                                      blank=True,
                                      width_field="width_field",
                                      height_field="height_field")
    height_field = models.IntegerField(default=0, null=True)
    width_field = models.IntegerField(default=0, null=True)

    campaign_relations = GenericRelation('campaigns.CampaignPartyRelation',
                                         related_query_name='campaign_relations_profiles')

    def __str__(self):
        return str(self.user) + ' | ' + str(self.name_prefix) + ' ' + str(self.first_name) + ' ' + str(self.last_name)
    # No other data for now


def create_user_profile(sender, instance, created, **kwargs):
    if created and not Profile.objects.filter(user=instance).exists():
        Profile.objects.create(user=instance)


post_save.connect(create_user_profile, sender=User, dispatch_uid="create_user_profile")

# Create your models here.
