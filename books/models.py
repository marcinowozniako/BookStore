from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Book(models.Model):
    book_id = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    authors = models.ManyToManyField('Author')
    published_year = models.CharField(max_length=12)
    acquired = models.BooleanField(default=False)
    thumbnail = models.URLField(blank=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['id']
