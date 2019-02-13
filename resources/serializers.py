from rest_framework import serializers
from .models import Book, Detail


class DetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Detail
        fields = '__all__'


class BookSerializer(serializers.ModelSerializer):
    detail = DetailSerializer(many=True)

    class Meta:
        model = Book
        fields = '__all__'

    def get_author(self, obj):
        return obj.user.username


class BookCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = [
            'author',
            'title'
        ]

