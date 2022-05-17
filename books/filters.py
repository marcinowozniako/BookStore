import django_filters
from django_filters import rest_framework as filters
from django_filters.widgets import RangeWidget

from books import models


class BookFilter(filters.FilterSet):
    title = filters.CharFilter()
    authors = filters.CharFilter()
    date_between = django_filters.DateFromToRangeFilter(
        field_name='published_date',
        label='Date (Between)',
        widget=RangeWidget(attrs={'type': 'date'})
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
