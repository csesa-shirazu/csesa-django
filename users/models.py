from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.contrib.auth.models import User

# from campaigns.models import CampaignPartyRelation
from django.db.models.signals import post_save


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="profile")

    campaign_relations = GenericRelation('campaigns.CampaignPartyRelation', related_query_name='campaign_relations_profiles')

    def __str__(self):
        return str(self.user)
    # No other data for now

def create_user_profile(sender, instance, created, **kwargs):
    if created and not Profile.objects.filter(user=instance).exists():
        Profile.objects.create(user=instance)


post_save.connect(create_user_profile, sender=User, dispatch_uid="create_user_profile")

# Create your models here.
