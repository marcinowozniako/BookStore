import django_filters
from django_filters import rest_framework as filters
from books import models


class BookFilter(filters.FilterSet):
    """
    Filter to allow user for filtering by these fields
    """
    book_id = filters.CharFilter(lookup_expr='icontains', label='External book_id')
    title = filters.CharFilter(lookup_expr='icontains', label='Title')
    authors = filters.CharFilter(field_name='authors__name', lookup_expr='icontains', label='Author')
    date = django_filters.RangeFilter(
        field_name='published_year',
        label='Date (Between)',
    )

    acquired = django_filters.BooleanFilter()

    class Meta:
        model = models.Book
        fields = [
            'title',
            'authors',
            'acquired',
        ]


class AuthorFilter(filters.FilterSet):
    """
    Filter to allow user for filtering by author of book
    """
    model = models.Author
    authors = filters.CharFilter(field_name='name', lookup_expr='icontains', label='Authors')
