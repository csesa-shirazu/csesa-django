from django.urls import path
from . import views

app_name = 'qualification'
urlpatterns = [
    path('cse-gradery', views.grader_qualification.as_view(), name='cse_gradery'),
]
