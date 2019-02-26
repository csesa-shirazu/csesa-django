from django.shortcuts import render
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import (
    BookSerializer,
    BookCreateSerializer,
    DetailCreateSerializer,
    DetailSerializer,
    RecommendationCreateSerializer,
)
from .models import Book
from users.models import Profile


class BookListAPIView(ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BookCreateView(APIView):
    serializer_class = BookCreateSerializer

    def post(self, request):
        out = BookCreateSerializer(data=request.data)
        if out.is_valid():
            instance = out.save()
            res = BookSerializer(instance)
            return Response(res.data, status=status.HTTP_200_OK)
        else:
            return Response(out.errors, status=status.HTTP_400_BAD_REQUEST)


class DetailCreateView(APIView):
    serializer_class = DetailCreateSerializer

    def post(self, request):
        out = DetailCreateSerializer(data=request.data)
        if out.is_valid():
            instance = out.save()
            res = DetailSerializer(instance)
            return Response(res.data, status=status.HTTP_200_OK)
        else:
            return Response(out.errors, status=status.HTTP_400_BAD_REQUEST)


class RecommendCreateView(APIView):
    serializer_class = RecommendationCreateSerializer

    def post(self, request):
        out = RecommendationCreateSerializer(data=request.data)
        if out.is_valid():
            instance = out.save()
            owner = Profile.objects.get(user__username=request.user.username)
            instance.owner = owner
            instance.save()
            return Response("ok", status=status.HTTP_200_OK)
        else:
            return Response(out.errors, status=status.HTTP_400_BAD_REQUEST)
