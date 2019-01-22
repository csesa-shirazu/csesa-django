from django.shortcuts import render

# Create your views here.
from rest_framework.generics import CreateAPIView


class GraderyRequestAPIView(CreateAPIView):
    pass
    # serializer_class = CampaignRequestEnrollmentSerializer
    #
    # def perform_create(self, serializer):
    #     user = self.request.user
    #
    #     try:
    #         obj = Campaign.objects.get(pk=self.kwargs['pk'])
    #     except Campaign.DoesNotExist:
    #         raise Http404
    #     if (CampaignPartyRelation.objects.filter(
    #             campaign=obj,
    #             content_type=ContentType.objects.get(model="profile"),
    #             object_id=user.profile.first().id
    #     ).exists()):
    #         raise ValidationError("Already a member")
    #     if (CampaignEnrollmentRequest.objects.filter(
    #             campaign=Campaign.objects.get(pk=self.kwargs['pk']),
    #             user=user,
    #     ).exists()):
    #         raise ValidationError("Already requested")
    #     serializer.save(
    #         campaign=Campaign.objects.get(pk=self.kwargs['pk']),
    #         user=user,
    #     )