from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.name


class Book(models.Model):
    book_id = models.CharField(max_length=255, blank=True)
    title = models.CharField(max_length=255, blank=True)
    authors = models.ManyToManyField('Author', blank=True)
    published_year = models.CharField(max_length=32, blank=True)
    acquired = models.BooleanField(default=False, blank=True)
    thumbnail = models.URLField(blank=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['id']
