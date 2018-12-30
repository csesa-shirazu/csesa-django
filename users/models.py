from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.contrib.auth.models import User

# from campaigns.models import CampaignPartyRelation


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="profile")

    campaign_relations = GenericRelation('campaigns.CampaignPartyRelation')

    def __str__(self):
        return str(self.user)
    # No other data for now

# Create your models here.
