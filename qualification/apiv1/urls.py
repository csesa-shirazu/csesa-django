from django.urls import path

from .views import (
    QualifiactionResultAPIView
)
app_name = 'qualification-api-v1'
urlpatterns = [
    path('result/<slug:slug>/<int:profile_id>', QualifiactionResultAPIView.as_view(), name='form'),
]
