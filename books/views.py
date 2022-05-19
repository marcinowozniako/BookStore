import django_filters
import requests
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle
from rest_framework.views import APIView

from books import models, filters, serializers


class BookListView(generics.ListCreateAPIView):
    queryset = models.Book.objects.all()
    serializer_class = serializers.BookSerializerList
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_class = filters.BookFilter

    def get_queryset(self):
        start_date = self.request.query_params.get('from', None)
        end_date = self.request.query_params.get('to', None)
        author = self.request.query_params.get('author', None)
        if start_date and end_date and author:
            qs = models.Book.objects.filter(published_year__range=[int(start_date), int(end_date)],
                                            authors__name__icontains=author)
            return qs
        elif start_date and end_date:
            qs = models.Book.objects.filter(published_year__range=[int(start_date), int(end_date)])
            return qs
        elif author:
            qs = models.Book.objects.filter(authors__name=author)
            return qs


class AuthorView(generics.ListCreateAPIView):
    queryset = models.Author.objects.all()
    serializer_class = serializers.AuthorSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_class = filters.AuthorFilter


class BookDetailsView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Book.objects.all()
    serializer_class = serializers.BookSerializerBase
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_class = filters.BookFilter


class ApiImportView(APIView):
    queryset = models.Book.objects.all()
    serializer_class = serializers.BookSerializerApiCreate

    def post(self, request):
        books1 = []
        updated_books = []
        r = requests.get(
            f"https://www.googleapis.com/books/v1/volumes?q=inauthor:{self.request.data['author']}&maxResults=40")
        if r.status_code == 200:
            response = r.json()
            nb = response.get('totalItems')
            idx = -40
            while nb > 0:
                idx += 40
                nb -= 40
                r = requests.get(
                    f"https://www.googleapis.com/books/v1/volumes?q=inauthor:{self.request.data['author']}&maxResults=40"
                    f"&startIndex={idx}")
                response = r.json()
                for book in response.get('items', ""):
                    book_id = book.get('id', "")
                    title = book['volumeInfo'].get('title', "")
                    published_year = book['volumeInfo'].get('publishedDate', "")
                    thumbnail = book['volumeInfo'].get('imageLinks', {}).get('thumbnail', "")

                    if not len(title) > 255:

                        books, created_b = models.Book.objects.update_or_create(
                            book_id=book_id,
                            title=title,
                            published_year=published_year,
                            thumbnail=thumbnail,
                            defaults={
                                'book_id': book_id,
                                'title': title,
                                'published_year': published_year,
                                'thumbnail': thumbnail
                            }
                        )
                        for author in book['volumeInfo'].get('authors', ""):
                            a, created_a = models.Author.objects.update_or_create(name=author)
                            books.authors.add(a)
                    if created_b:
                        books1.append(books)
                    if not created_b:
                        updated_books.append(books)

            return Response({'imported': len(books1), 'updated': len(updated_books)})

        else:
            return Response({'Error': 'Connection Error'})
