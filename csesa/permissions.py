from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerOfCampaignPartyRelationOrReadOnly(BasePermission):
    message = 'You must be the owner of this object.'

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_authenticated and obj.content_object == request.user.profile.first()