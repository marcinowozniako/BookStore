from django.urls import reverse_lazy
from django.utils.safestring import mark_safe
from rest_framework import serializers

from books.models import Author, Book


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ('id', 'name')


class BookSerializerBase(serializers.ModelSerializer):
    authors = serializers.SlugRelatedField(many=True, slug_field='name', queryset=Author.objects.all())

    class Meta:
        model = Book
        fields = (
            'id',
            'book_id',
            'title',
            'authors',
            'published_year',
            'acquired',
            'thumbnail',
        )


class BookSerializerList(BookSerializerBase):
    authors = serializers.SlugRelatedField(many=True, slug_field='name', queryset=Author.objects.all(),
                                           help_text=mark_safe(
                                               f"<a href='{'authors'}'>Add Authors</a>")
                                           )


class BookSerializerApiCreate(serializers.ModelSerializer):
    # authors = serializers.HyperlinkedModelSerializer(many=True)
    author = serializers.CharField()

    class Meta:
        model = Book
        fields = ('authors',)
