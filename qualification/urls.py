from django.urls import path
from . import views

app_name = 'qualification'
urlpatterns = [
    path('gradery-no-vote-list/', views.gradery_no_vote.as_view(), name='gradery_no_vote'),
    path('<slug:slug>/result/', views.result_view.as_view(), name='result'),
    path('<slug:slug>/', views.qualification_view.as_view(), name='form'),
]
