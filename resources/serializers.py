from rest_framework import serializers
from .models import (
    Book,
    Detail,
    Publisher,
    Recommendation,
)
from users.models import Profile
from rest_framework.exceptions import ValidationError


class PublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publisher
        fields = [
            'name',
        ]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = [
            'first_name',
            'last_name'
        ]


class DetailSerializer(serializers.ModelSerializer):
    publisher = PublisherSerializer()
    translator = UserSerializer(many=True)

    class Meta:
        model = Detail
        fields = [
            'publisher',
            'translator',
            'version',
        ]


class BookSerializer(serializers.ModelSerializer):
    details = DetailSerializer(many=True)
    author = UserSerializer(many=True)

    class Meta:
        model = Book
        fields = [
            'id',
            'details',
            'title',
            'author'
        ]


class BookCreateSerializer(serializers.ModelSerializer):
    author = UserSerializer(many=True)

    class Meta:
        model = Book
        fields = [
            'author',
            'title'
        ]

    def validate(self, attrs):
        title = attrs['title']
        qs = Book.objects.filter(title=title)
        if qs.exists():
            raise ValidationError("this origin exists already")
        authors = attrs['author']
        for author in authors:
            qs = Profile.objects.filter(first_name=author['first_name'], last_name=author['last_name'])
            if not qs.exists():
                raise ValidationError("author not found")
        return attrs

    def create(self, validated_data):
        instance = Book(title=validated_data["title"])
        instance.save()
        authors = validated_data['author']
        for author in authors:
            person = Profile.objects.get(first_name=author['first_name'], last_name=author['last_name'])
            instance.author.add(person)
        instance.save()
        return instance


class DetailCreateSerializer(serializers.ModelSerializer):
    translator = UserSerializer(many=True)
    publisher = PublisherSerializer()
    book = serializers.CharField(max_length=50)

    class Meta:
        model = Detail
        fields = [
            'translator',
            'publisher',
            'book',
            'version',
        ]

    def validate(self, attrs):
        translators = attrs['translator']
        for translator in translators:
            person = Profile.objects.filter(first_name=translator['first_name'], last_name=translator['last_name'])
            if not person.exists():
                raise ValidationError("translator not found")
        title = attrs['book']
        book = Book.objects.filter(title=title)
        if not book.exists():
            raise ValidationError("book not found")
        name = attrs['publisher']['name']
        publisher = Publisher.objects.filter(name=name)
        if not publisher.exists():
            raise ValidationError("publisher not found")
        return attrs

    def create(self, validated_data):
        instance = Detail(version=validated_data["version"])
        book = Book.objects.get(title=validated_data["book"])
        instance.book = book
        publisher = Publisher.objects.get(name=validated_data['publisher']['name'])
        instance.publisher = publisher
        instance.save()
        translators = validated_data["translator"]
        for trans in translators:
            person = Profile.objects.get(first_name=trans["first_name"], last_name=trans["last_name"])
            instance.translator.add(person)
        instance.save()
        return instance


class RecommendationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recommendation
