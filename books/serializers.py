from rest_framework import serializers
from books import models


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Author
        fields = ('id', 'name')


class BookSerializer(serializers.ModelSerializer):
    authors = serializers.StringRelatedField(many=True)
    identifiers = serializers.StringRelatedField(many=True)

    class Meta:
        model = models.Book
        fields = (
            'book_id',
            'title',
            'authors',
            'published_date',
            'acquired',
        )
