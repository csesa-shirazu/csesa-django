from django.urls import path

from .views import (
    QualifiactionResultAPIView
)
app_name = 'qualification-api-v1'
urlpatterns = [
    path('result/<slug:slug>/<str:username>', QualifiactionResultAPIView.as_view(), name='form'),
]
