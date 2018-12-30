from django.urls import path
from . import views

app_name = 'qualification'
urlpatterns = [
    path('<slug:slug>', views.qualification_view.as_view(), name='form'),
]
