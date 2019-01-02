import json, random, string

from django.contrib.contenttypes.models import ContentType

from campaigns.models import CampaignPartyRelation, CampaignPartyRelationType, Campaign
from csecourses.models import CSECourse, CSECourseGroup, CSECourseGroupTerm, CSETerm
from users.models import Profile, User


def rand_string():
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
        pas = rand_string()
        user = profile.user
        user.set_password(pas)
        user.save()

        f.write(user.username + "\n")
        f.write(pas + "\n")
    f.close()


# Temporary and bad function!
def read_teachers():
    f = json.loads(open('cse-data/course_teachers_97_1st.json', 'r').read())
    for x in f:
        qs = User.objects.filter(last_name=f[x]['teacher_name'])
        if qs.exists():
            u = qs.first()
        else:
            while True:
                try:
                    u = User.objects.create(
                        username=rand_string(),
                        last_name=f[x]['teacher_name']
                    )
                    break
                except:
                    continue
        p = u.profile.first()
        c = CSECourse.objects.get(cse_id=x.split('^')[0])
        cg = CSECourseGroup.objects.get(course=c, group=int(x.split('^')[1]))
        cgt = CSECourseGroupTerm.objects.get(term=CSETerm.objects.first(), course_group=cg)
        the_campaign = Campaign.objects.get(course_data=cgt)
        if not CampaignPartyRelation.objects.filter(
                campaign=the_campaign,
                content_type=ContentType.objects.get_for_model(p),
                object_id=p.id,
                type=CampaignPartyRelationType.GRADER
        ).exists():
            CampaignPartyRelation.objects.create(
                campaign=the_campaign,
                content_object=p,
                type=CampaignPartyRelationType.GRADER
            )
