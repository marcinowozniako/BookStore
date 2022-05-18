import django_filters
from django_filters import rest_framework as filters
from books import models


class BookFilter(filters.FilterSet):
    book_id = filters.CharFilter(lookup_expr='icontains', label='External book_id')
    title = filters.CharFilter(lookup_expr='icontains', label='Title')
    authors = filters.CharFilter(field_name='authors__name', lookup_expr='icontains', label='Authors')
    date_between = django_filters.RangeFilter(
        field_name='published_year',
        label='Date (Between)',
    )
    acquired = django_filters.BooleanFilter()

    class Meta:
        model = models.Book
        fields = [
            'title',
            'authors',
            'date_between',
            'acquired',
        ]


class AuthorFilter(filters.FilterSet):
    model = models.Author
    authors = filters.CharFilter(field_name='name', lookup_expr='icontains', label='Authors')