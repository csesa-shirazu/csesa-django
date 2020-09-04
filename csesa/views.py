from django.contrib.contenttypes.models import ContentType
from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import ValidationError
from rest_framework.generics import CreateAPIView, DestroyAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.utils import json
from rest_framework.views import APIView

from campaigns.models import CampaignPartyRelation, CampaignPartyRelationType, Campaign, CampaignPartyRelationStatus
from campaigns.serializers import GraderRelationSerializer, CampaignAsCourseSimpleSerializer, \
    CampaignGraderyRequestSerializer
from csecourses.models import CSECourseGroupTerm, CSECourseGroup, CSETerm
from csesa.permissions import IsOwnerOfCampaignPartyRelationOrReadOnly
from csesa.serializers import GraderOfCourseRelationSerializer
from csesa.utils import arabic_chars_to_persian, get_prev_term, get_cur_term
from users.models import User, Profile
from users.serializers import ProfileRetrieveSimpleSerializer


def index_view(request):
    return redirect(reverse('qualification:result', kwargs={'slug': 'cse-gradery'}))
    # if request.user.is_authenticated:
    #     return redirect(reverse('qualification:form', kwargs={'slug': 'cse-gradery'}))
    # else:
    #     return redirect(
    #         reverse('users:login') + "?next=" + reverse('qualification:form', kwargs={'slug': 'cse-gradery'}))


def graders_view(request, term_title):
    if request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser):

        try:
            the_term = CSETerm.objects.get(title=term_title)
        except CSETerm.DoesNotExist:
            raise Http404

        context = {}
        if 'gid' in request.POST:
            try:
                the_grader = User.objects.get(username=request.POST['gid']).profile.first()
            except User.DoesNotExist:
                context['message'] = 'پروفایل با این یوزرنیم وجود ندارد'
            else:
                try:
                    the_campaign = Campaign.objects.get(id=request.POST['cid'])
                except Campaign.DoesNotExist:
                    context['message'] = 'درس وارد شده نامعتبر است'
                else:
                    grader_qs = CampaignPartyRelation.objects.filter(
                            campaign=the_campaign,
                            content_type=ContentType.objects.get_for_model(the_grader),
                            object_id=the_grader.id,
                            type=CampaignPartyRelationType.GRADER,
                    )
                    if grader_qs.exists():
                        grader_relation = grader_qs.first()
                        if grader_relation.status != CampaignPartyRelationStatus.APPROVED:
                            grader_relation.status = CampaignPartyRelationStatus.APPROVED
                            grader_relation.save()
                            context['message'] = 'گریدر از قبل وارد شده'
                        else:
                            context['message'] = 'گریدر از قبل وارد شده'
                    else:
                        CampaignPartyRelation.objects.create(
                            campaign=the_campaign,
                            content_type=ContentType.objects.get_for_model(the_grader),
                            object_id=the_grader.id,
                            type=CampaignPartyRelationType.GRADER,
                            status=CampaignPartyRelationStatus.APPROVED
                        )
                        context['message'] = 'با موفقیت ثبت شد'

        context.update({
            'gcrs': GraderRelationSerializer(
                CampaignPartyRelation.objects.filter(
                    type=CampaignPartyRelationType.GRADER,
                    campaign__course_data__term = the_term,
                    # status=CampaignPartyRelationStatus.APPROVED
                ), many=True
            ).data,
            'courses': CampaignAsCourseSimpleSerializer(
                Campaign.objects.filter(
                    course_data__term = the_term
                ),
                many=True
            ).data
        })
        return render(request, "graders.html", context)
    raise Http404


class GradersWithQualificationAPIView(APIView):
    authentication_class = []  # Don't forget to add a 'comma' after first element to make it a tuple

    permission_classes = [AllowAny]

    def get(self, request, format=None):
        data = ProfileRetrieveSimpleSerializer(
            Profile.objects.filter(campaign_relations__in=CampaignPartyRelation.objects.filter(
                content_type=ContentType.objects.get(model='profile'),
                type=CampaignPartyRelationType.GRADER,
                dst_qualifications__isnull=False
            ).all()).distinct().order_by('-id'), many=True).data

        return Response(data)


class CourseGroupListAPIView(APIView):
    authentication_class = []  # Don't forget to add a 'comma' after first element to make it a tuple

    permission_classes = [AllowAny]

    def get(self, request, format=None):
        data = [
            {
                'id': course_group.id,
                'title_fa': arabic_chars_to_persian(str(course_group)),
            }
            for course_group in CSECourseGroup.objects.all()
        ]

        return Response(data)


class CourseGroupTAsAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [AllowAny]

    def get(self, request, pk=None, format=None):
        try:
            course_group = CSECourseGroup.objects.get(pk=pk)
        except:
            raise Http404
        print(pk)

        try:
            course_data = CSECourseGroupTerm.objects.get(
                course_group=course_group,
                term=get_prev_term()
            )
            prev_campaign = Campaign.objects.get(course_data=course_data)
        except:
            prev_term_graders = []
            prev_is_teacher = False
        else:

            prev_is_teacher = request.user.is_authenticated and CampaignPartyRelation.objects.filter(
                campaign=prev_campaign,
                content_type=ContentType.objects.get(model="profile"),
                object_id=request.user.profile.first().id,
                type=CampaignPartyRelationType.TEACHER
            ).exists()

            prev_term_graders = GraderOfCourseRelationSerializer(
                CampaignPartyRelation.objects.filter(
                    campaign=prev_campaign,
                    content_type=ContentType.objects.get(model='profile'),
                    type=CampaignPartyRelationType.GRADER,
                    status=CampaignPartyRelationStatus.APPROVED,
                ).all(), context={
                    'request': request,
                    'is_teacher': prev_is_teacher
                }
                , many=True).data

        try:
            course_data = CSECourseGroupTerm.objects.get(
                course_group=course_group,
                term=get_cur_term()
            )
            cur_campaign = Campaign.objects.get(course_data=course_data)
        except:
            cur_term_graders = []
            is_teacher = False
        else:

            is_teacher = request.user.is_authenticated and CampaignPartyRelation.objects.filter(
                campaign=cur_campaign,
                content_type=ContentType.objects.get(model="profile"),
                object_id=request.user.profile.first().id,
                type=CampaignPartyRelationType.TEACHER
            ).exists()

            cur_term_graders = GraderOfCourseRelationSerializer(
                CampaignPartyRelation.objects.filter(
                    campaign=cur_campaign,
                    content_type=ContentType.objects.get(model='profile'),
                    type=CampaignPartyRelationType.GRADER
                ).all(), context={
                    'request': request,
                    'is_teacher': is_teacher
                }, many=True).data


        data = {
            'course_group': {
                'id': course_group.id,
                'title_fa': arabic_chars_to_persian(str(course_group)),
            },
            'prev_term_graders': prev_term_graders,
            'cur_term_graders': cur_term_graders,
            'is_teacher': is_teacher
        }

        return Response(data)


class GraderyRequestAPIView(CreateAPIView):
    serializer_class = CampaignGraderyRequestSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    # def create(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     status = self.perform_create(serializer)
    #     headers = self.get_success_headers(serializer.data)
    #     return Response({"result": "success"}, status=status, headers=headers)

    def perform_create(self, serializer):
        profile = self.request.user.profile.first()

        try:
            obj = Campaign.objects.get(
                course_data=CSECourseGroupTerm.objects.get(
                    course_group=CSECourseGroup.objects.get(
                        pk=self.kwargs['pk']
                    ),
                    term=get_cur_term()
                )
            )
        except:
            raise Http404
        cpr_qs = CampaignPartyRelation.objects.filter(
            campaign=obj,
            content_type=ContentType.objects.get(model="profile"),
            object_id=profile.id,
            type=CampaignPartyRelationType.GRADER,
        )
        if (cpr_qs.exists()):
            grader_cpr = cpr_qs.first()
            if grader_cpr.status == CampaignPartyRelationStatus.PENDING:
                print("hello")
                grader_cpr.enrollment_request_note = serializer.validated_data['enrollment_request_note']
                grader_cpr.save()  # TODO: seperate update. VERY BAD IMPLEMENTATION JUST BECAUSE OF LACK OF TIME
                return status.HTTP_202_ACCEPTED
            raise ValidationError("Already requested")
        else:
            serializer.save(
                campaign=obj,
                content_object=profile,
                type=CampaignPartyRelationType.GRADER,
                status=CampaignPartyRelationStatus.PENDING
            )
            return status.HTTP_201_CREATED


class DestroyGraderyRequestAPIView(DestroyAPIView):
    serializer_class = CampaignGraderyRequestSerializer
    lookup_field = 'id'
    queryset = CampaignPartyRelation.objects.all()
    permission_classes = [IsOwnerOfCampaignPartyRelationOrReadOnly]
    authentication_classes = [TokenAuthentication]


class AcceptTAAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None, format=None):
        try:
            cpr = CampaignPartyRelation.objects.get(pk=pk)
        except:
            raise Http404
        profile = request.user.profile.first()
        if not CampaignPartyRelation.objects.filter(
                campaign=cpr.campaign,
                content_type=ContentType.objects.get(model='profile'),
                object_id=profile.id,
                type=CampaignPartyRelationType.TEACHER
        ).exists():
            return Response({'result': 'Not Allowed'}, status=status.HTTP_403_FORBIDDEN)
        cpr.status = CampaignPartyRelationStatus.APPROVED
        cpr.save()
        return Response({'result': 'success'}, status=status.HTTP_200_OK)

class RejectTAAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None, format=None):
        try:
            cpr = CampaignPartyRelation.objects.get(pk=pk)
        except:
            raise Http404
        profile = request.user.profile.first()
        if not CampaignPartyRelation.objects.filter(
                campaign=cpr.campaign,
                content_type=ContentType.objects.get(model='profile'),
                object_id=profile.id,
                type=CampaignPartyRelationType.TEACHER
        ).exists():
            return Response({'result': 'Not Allowed'}, status=status.HTTP_403_FORBIDDEN)
        cpr.status = CampaignPartyRelationStatus.REJECTED
        cpr.save()
        return Response({'result': 'success'}, status=status.HTTP_200_OK)
