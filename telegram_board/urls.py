from django.urls import path
from . import views

app_name = 'telegram_board'
urlpatterns = [
    path('send/', views.send_message.as_view(), name='send'),
]