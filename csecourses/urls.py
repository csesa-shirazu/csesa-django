from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from csecourses.views import GraderyRequestAPIView
from . import views

app_name = 'csecourses'
urlpatterns = [
    path('<int:pk>/request-enrollment/', GraderyRequestAPIView.as_view(), name='request-enrollment'),
]