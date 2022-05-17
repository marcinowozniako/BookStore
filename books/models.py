from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=255)
    books = models.ManyToManyField('Book', related_name='authors', blank=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=255)
    books = models.ManyToManyField('Book', related_name='categories', blank=True)

    def __str__(self):
        return self.name


class Book(models.Model):
    book_id = models.CharField(max_length=255, unique=True)
    title = models.CharField(max_length=255)
    published_date = models.CharField(max_length=12)
    acquired = models.BooleanField(default=False)

    def __str__(self):
        return self.title
