import random, string

from django.contrib.contenttypes.models import ContentType

from campaigns.models import CampaignPartyRelation, CampaignPartyRelationType
from users.models import Profile


def randpass():
    pas = ""
    for i in range(5):
        pas += random.choice(string.ascii_letters)
    return pas

def set_passwords():

    # Get all students (with at least one course)
    profiles = Profile.objects.filter(campaign_relations__in=CampaignPartyRelation.objects.filter(
        content_type=ContentType.objects.get(model='profile'),
        type=CampaignPartyRelationType.STUDENT
    ).all()).all().distinct()

    f = open('cse-data/up.txt', 'w')
    for profile in profiles:
        pas = randpass()
        user = profile.user
        user.set_password(pas)
        user.save()

        f.write(user.username + "\n")
        f.write(pas + "\n")
    f.close()