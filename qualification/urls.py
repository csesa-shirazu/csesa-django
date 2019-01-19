from django.urls import path
from . import views

app_name = 'qualification'
urlpatterns = [
    path('<slug:slug>/result/', views.result_view.as_view(), name='form'),
    path('<slug:slug>', views.qualification_view.as_view(), name='form'),
]
