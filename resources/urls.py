from django.urls import path

from .views import (
    BookListAPIView,
    BookCreateView
)
app_name = 'qualification-api-v1'
urlpatterns = [
    path('books/showall/', BookListAPIView.as_view(), name='list'),
    path('books/create/', BookCreateView.as_view(), name='create')
]
