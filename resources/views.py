from django.shortcuts import render
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.views import APIView
from .serializers import (
    BookSerializer,
    BookCreateSerializer
)
from .models import Book


class BookListAPIView(ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BookCreateView(CreateAPIView):
    serializer_class = BookCreateSerializer
