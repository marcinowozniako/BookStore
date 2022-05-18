import django_filters
from rest_framework import generics, permissions
from rest_framework.views import APIView

from books import models, filters, serializers


class BookListView(generics.ListCreateAPIView):
    queryset = models.Book.objects.all()
    serializer_class = serializers.BookSerializerList
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_class = filters.BookFilter


class AuthorView(generics.ListCreateAPIView):
    queryset = models.Author.objects.all()
    serializer_class = serializers.AuthorSerializer


class BookDetailsView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Book.objects.all()
    serializer_class = serializers.BookSerializerBase
    lookup_field = 'book_id'
