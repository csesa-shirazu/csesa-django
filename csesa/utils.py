import json, random, string

from django.contrib.contenttypes.models import ContentType

from campaigns.models import CampaignPartyRelation, CampaignPartyRelationType, Campaign, CampaignPartyRelationStatus, \
    CampaignType
from csecourses.models import CSECourse, CSECourseGroup, CSECourseGroupTerm, CSETerm
from users.models import Profile, User


def rand_string():
    pas = ""
    for i in range(5):
        pas += random.choice(string.ascii_lowercase)
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


# Temporary and bad function!
def read_courses(stdno):
    u = User.objects.get(username=stdno)
    p = u.profile.first()
    f = json.loads(open('cse-data/course_students_97_1st.json', 'r').read())
    for x in f:
        found = False

        for k in f[x]['students']:
            if k['first_name'] == u.first_name and k['family_name'] == u.last_name:
                found = True
                break

        if not found:
            continue

        print(f[x]['name'])

        c = CSECourse.objects.get(cse_id=x.split('^')[0])
        cg = CSECourseGroup.objects.get(course=c, group=int(x.split('^')[1]))
        cgt = CSECourseGroupTerm.objects.get(term=CSETerm.objects.first(), course_group=cg)
        the_campaign = Campaign.objects.get(course_data=cgt)
        if not CampaignPartyRelation.objects.filter(
                campaign=the_campaign,
                content_type=ContentType.objects.get_for_model(p),
                object_id=p.id,
                type=CampaignPartyRelationType.STUDENT
        ).exists():
            CampaignPartyRelation.objects.create(
                campaign=the_campaign,
                content_object=p,
                type=CampaignPartyRelationType.STUDENT
            )


def arabic_chars_to_persian(ar_str):
    return ar_str.replace('ك', 'ک').replace('ي', 'ی')


def get_user_profile_names():
    for user in User.objects.all():
        p = user.profile.first()
        if not p.first_name:
            if 'دکتر' in user.first_name:
                user.first_name = user.first_name[5:]
                user.save()
                p.name_prefix = 'دکتر'
            p.first_name = arabic_chars_to_persian(user.first_name)
            p.last_name = arabic_chars_to_persian(user.last_name)
            p.save()


def set_teacher_campaign_relations():
    for user in User.objects.all():
        p = user.profile.first()
        if p.name_prefix == 'دکتر':
            for cpr in p.campaign_relations.all():
                cpr.type = CampaignPartyRelationType.TEACHER
                cpr.save()

def get_prev_term():
    return CSETerm.objects.get(pk = 2)  # TODO: correct logic


def get_cur_term():
    return CSETerm.objects.last()  # TODO: correct logic

def read_course_students(file_name):
    file = open(file_name, 'r')
    f = json.loads(file.read())
    file.close()
    for x in f.keys():
        try:
            the_course = CSECourse.objects.get(cse_id=x.split('^')[0])
        except:
            the_course = CSECourse.objects.create(
                cse_id=x.split('^')[0],
                title=f[x]['title'],
            )
        else:
            the_course.title = f[x]['title']
            the_course.save()
        try:
            the_course_group = CSECourseGroup.objects.get(
                course=the_course,
                group=int(x.split('^')[1])
            )
        except:
            the_course_group = CSECourseGroup.objects.create(
                course=the_course,
                group=int(x.split('^')[1])
            )
        try:
            the_course_group_term = CSECourseGroupTerm.objects.get(
                course_group=the_course_group,
                term=CSETerm.objects.last()
            )
        except:
            the_course_group_term = CSECourseGroupTerm.objects.create(
                course_group=the_course_group,
                term=CSETerm.objects.last()
            )
        try:
            the_campaign = Campaign.objects.get(
                course_data=the_course_group_term
            )
        except:
            the_campaign = Campaign.objects.create(
                course_data=the_course_group_term,
                type=CampaignType.COURSE
            )

        teachers_string_arr = f[x]['teacher'].split('*')
        
        for i in range(0,len(teachers_string_arr), 3):

            if(i + 1 >= len(teachers_string_arr)):
                break

            teachers_qs = User.objects.filter(
                first_name = teachers_string_arr[i + 1],
                last_name = teachers_string_arr[i],
            )
            if teachers_qs.exists():
                teacher = teachers_qs.first()
            else:
                teacher = User.objects.create(
                    username=rand_string(),
                    first_name = teachers_string_arr[i + 1],
                    last_name = teachers_string_arr[i]
                )
            teacher_profile = teacher.profile.first()
            if not CampaignPartyRelation.objects.filter(
                campaign=the_campaign,
                content_type=ContentType.objects.get_for_model(teacher_profile),
                object_id=teacher_profile.id,
                type=CampaignPartyRelationType.TEACHER,
                status=CampaignPartyRelationStatus.APPROVED
            ).exists():
                CampaignPartyRelation.objects.create(
                    campaign=the_campaign,
                    content_object=teacher.profile.first(),
                    type=CampaignPartyRelationType.TEACHER,
                    status=CampaignPartyRelationStatus.APPROVED
                )
        #  for s in f[x]['students']:
        #      p = None
        #      try:
        #          p = Profile.objects.get(user__first_name=s['first_name'], user__last_name=s['family_name'])
        #      except:
        #          username = rand_string()
        #          while User.objects.filter(username=username).exists():
        #              username = rand_string()
        #          u = User.objects.create(username=username, first_name=s['first_name'], last_name=s['family_name'])
        #          p = u.profile.first()
        #      if(not CampaignPartyRelation.objects.filter(
        #          campaign=the_campaign,
        #          object_id=p.id,
        #          content_type=ContentType.objects.get_for_model(Profile),
        #          type=CampaignPartyRelationType.STUDENT
        #      ).exists()):
        #          CampaignPartyRelation.objects.create(
        #              campaign=the_campaign,
        #              content_object=p,
        #              type=CampaignPartyRelationType.STUDENT,
        #              status=CampaignPartyRelationStatus.APPROVED
        #          )