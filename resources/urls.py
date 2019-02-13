from django.urls import path

from .views import BookCreateAPIView
app_name = 'qualification-api-v1'
urlpatterns = [
    path('books/create/', BookCreateAPIView.as_view(), name='create'),
]
