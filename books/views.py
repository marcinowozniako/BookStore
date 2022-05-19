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
        if start_date:
            qs = models.Book.objects.filter(published_year__range=[int(start_date), int(end_date)])
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
    throttle_classes = [UserRateThrottle]

    def post(self, request):
        authorss = []
        books1 = []
        books2 = []
        r = requests.get(
            f"https://www.googleapis.com/books/v1/volumes?q=inauthor:{self.request.POST['authors']}&maxResults=40")
        if r.status_code == 200:
            response = r.json()
            nb = response.get('totalItems')
            idx = 0
            while nb >= 0:
                idx += 40
                nb -= 40

                r = requests.get(
                    f"https://www.googleapis.com/books/v1/volumes?q=inauthor:{self.request.POST['authors']}&maxResults=40"
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
                            if created_a:
                                authorss.append(a)
                            books.authors.add(a)
                    if created_b:
                        books1.append(books)

            return Response({'imported': len(books1)})

        else:
            return Response({'Error': 'Connection Error'})

