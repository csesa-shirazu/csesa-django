from rest_framework.serializers import (
    ModelSerializer
)

from qualification.models import Qualification


class QualifiactionResult(ModelSerializer):
    class Meta:
        model = Qualification
        fields = [
            'id'
        ]