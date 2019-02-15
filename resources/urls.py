from django.urls import path

from .views import (
    BookListAPIView,
    BookCreateView,
    DetailCreateView
)
app_name = 'qualification-api-v1'
urlpatterns = [
    path('books/showall/', BookListAPIView.as_view(), name='list'),
    path('origin/create/', BookCreateView.as_view(), name='create_origin'),
    path('books/create/', DetailCreateView.as_view(), name='create_book'),
]
