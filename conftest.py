import pytest
from rest_framework.test import APIClient

import books.models
from books import models


@pytest.fixture
def client_api():
    """
    Django Rest client Instance
    """
    client_api = APIClient()
    return client_api


@pytest.fixture
def created_author(db):
    """
    Fixture for all tests which require Author to be created
    """
    author = books.models.Author.objects.create(name='J.R.R Tolkien')
    author1 = books.models.Author.objects.create(name='C.S Lewis')
    return author, author1


@pytest.fixture
def created_book(db, created_author):
    """
    Fixture for all test which require book to be created
    """
    book = books.models.Book.objects.create(book_id='ywu12', title='Hobbit', acquired=False, thumbnail='',
                                            published_year='2001')
    book1 = books.models.Book.objects.create(book_id='ywu123', title='Narnia', acquired=True, thumbnail='',
                                             published_year='2021')
    book.authors.add(created_author[0])
    book1.authors.add(created_author[1])
    return book, book1

