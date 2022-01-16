import json, random, string

from django.contrib.contenttypes.models import ContentType
from django.db.models import Model

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

def presian_chars_to_arabic(fa_str):
    return fa_str.replace('ک', 'ك').replace('ی', 'ي')

def presian_chars_to_arabic_only_y(fa_str):
    return fa_str.replace('ی', 'ي')

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


def get_cur_term():
    return CSETerm.objects.last()  # TODO: correct logic

def get_prev_term():
    terms = CSETerm.objects.all()
    return terms[len(terms) - 1]  # TODO: correct logic



def read_course_data(file_name, cse_term, read_students):
    file = open(file_name, 'r')
    f = json.loads(file.read())
    file.close()
    for x in f.keys():
        try:
            the_course = CSECourse.objects.get(cse_id=x.split('^')[0])
        except CSECourse.DoesNotExist:
            the_course = CSECourse.objects.create(
                cse_id=x.split('^')[0],
                title=f[x]['title'],
            )
        except:
            print(f[x]['title'])
            continue
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
                term=cse_term
            )
        except:
            the_course_group_term = CSECourseGroupTerm.objects.create(
                course_group=the_course_group,
                term=cse_term
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

        for i in range(0, len(teachers_string_arr), 3):

            if (i + 1 >= len(teachers_string_arr)):
                break
            teacher_first_name = teachers_string_arr[i + 1]
            teacher_last_name = teachers_string_arr[i]
            teachers_qs = User.objects.filter(
                first_name__in = [teacher_first_name, presian_chars_to_arabic_only_y(teacher_first_name), presian_chars_to_arabic(teacher_first_name)],
                last_name__in = [teacher_last_name, presian_chars_to_arabic_only_y(teacher_last_name), presian_chars_to_arabic(teacher_last_name)],
            )
            if teachers_qs.exists():
                teacher = teachers_qs.first()
            else:
                teacher = User.objects.create(
                    username=rand_string(),
                    first_name=teacher_first_name,
                    last_name=teacher_last_name
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

        if read_students:
            for s in f[x]['students']:
                first_name = s[0].strip()
                last_name =  s[1].strip()
                p = None
                try:
                    p = Profile.objects.get(user__first_name__in=[presian_chars_to_arabic(first_name), presian_chars_to_arabic_only_y(first_name), first_name], user__last_name__in=[presian_chars_to_arabic(last_name), presian_chars_to_arabic_only_y(last_name), last_name])
                except Profile.DoesNotExist:
                    username = rand_string()
                    while User.objects.filter(username=username).exists():
                        username = rand_string()
                    u = User.objects.create(username=username, first_name=first_name, last_name=last_name.strip())
                    p = u.profile.first()
                except:
                    print(first_name + ' ' + last_name)
                    continue
                if (not CampaignPartyRelation.objects.filter(
                        campaign=the_campaign,
                        object_id=p.id,
                        content_type=ContentType.objects.get_for_model(Profile),
                        type=CampaignPartyRelationType.STUDENT
                ).exists()):
                    CampaignPartyRelation.objects.create(
                        campaign=the_campaign,
                        content_object=p,
                        type=CampaignPartyRelationType.STUDENT,
                        status=CampaignPartyRelationStatus.APPROVED
                    )

def read_new_stds(stds):
    """
        stds is like اصغري,اصغر,4003333\n.....
    """
    x = ""
    for std in stds.split("\n"):
        stdd = std.split(',')
        u = User.objects.create(last_name=stdd[0], first_name=stdd[1], username=stdd[2])
        pss = rand_string()
        u.set_password(pss)
        u.save()
        x += stdd[2] + '\n' + pss + '\n'
    print(x)