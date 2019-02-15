from rest_framework import serializers
from .models import Book, Detail, Publisher
from users.models import Profile
from rest_framework.exceptions import ValidationError


class PublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publisher
        fields = [
            'name',
        ]


class DetailSerializer(serializers.ModelSerializer):
    publisher = PublisherSerializer()

    class Meta:
        model = Detail
        fields = [
            'publisher',
            'translator',
            'version',
        ]


class BookSerializer(serializers.ModelSerializer):
    details = DetailSerializer(many=True)
    author = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = [
            'id',
            'details',
            'title',
            'author'
        ]

    def get_author(self, obj):
        return obj.author.user.username


class BookCreateSerializer(serializers.ModelSerializer):
    author_pk = serializers.IntegerField()

    class Meta:
        model = Book
        fields = [
            'author_pk',
            'title'
        ]

    def validate(self, attrs):
        author = Profile.objects.filter(pk=attrs["author_pk"])
        if author.exists():
            return attrs
        else:
            return ValidationError("author not found")

    def create(self, validated_data):
        author = Profile.objects.get(pk=validated_data["author_pk"])
        instance = Book(author=author, title=validated_data["title"])
        instance.save()
        return instance


class DetailCreateSerializer(serializers.ModelSerializer):
    publisher = serializers.IntegerField()
    book = serializers.IntegerField()

    class Meta:
        model = Detail
        fields = [
            'publisher',
            'book',
            'version',
        ]

    def validate(self, attrs):
        qs = Publisher.objects.filter(pk=attrs['publisher'])
        if qs.exists():
            qs = Book.objects.filter(pk=attrs['book'])
            if qs.exists():
                return attrs
            else:
                raise ValidationError("book not found")
        else:
            raise ValidationError("publisher not found")

    def create(self, validated_data):
        publisher = Publisher.objects.get(pk=validated_data["publisher"])
        book = Book.objects.get(pk=validated_data["book"])
        instance = Detail(publisher=publisher, version=validated_data["version"], book=book)
        instance.save()
        return instance
