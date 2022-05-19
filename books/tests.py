from . import models


def test_book_list_page(client_api, created_book):
    """
    Test to check if page show list of books
    """
    response = client_api.get('/books/', {}, format='json')

    assert response.status_code == 200
    assert models.Book.objects.count() == len(response.data)


def test_import_page(client_api, db):
    """
    Test to check if import page importing books from GoogleAPI
    """
    response = client_api.post('/books/import', {'author': 'J.R.R Tolkien'}, format='json')

    assert response.status_code == 200
    assert response.data['imported'] == models.Book.objects.count()


def test_authors_page(client_api, created_author):
    """
    Test to check if authors page show list of authors
    """
    response = client_api.get('/books/authors', {}, format='json')

    assert response.status_code == 200
    assert models.Author.objects.all().count() == len(response.data)


def test_authors_add_page(client_api, db):
    """
    Test to check if user can add new author
    """
    response = client_api.post('/books/authors', {'name': 'C.S Lewis'}, format='json')

    assert response.status_code == 201
    assert models.Author.objects.all().count() == 1


def test_add_book_page(client_api, created_author):
    """
    Test to check if user can add new book
    """
    response = client_api.post('/books/', {
        "book_id": "ywu12",
        "title": "Hobbit",
        "acquired": False,
        "thumbnail": "",
        "published_year": "2001",
        "authors": [created_author[0].name]
    }, format='json')

    assert response.status_code == 201
    assert models.Book.objects.count() == 1


def test_details_book_page(client_api, created_book):
    """
    Test to check if page show details of book
    """
    response = client_api.get(f'/books/{created_book[0].id}', {}, format='json')

    assert response.status_code == 200
    assert models.Book.objects.values('acquired')[0].get('acquired') == False


def test_detail_book_page_patch(client_api, created_book):
    """
    Test to check if user can modify book
    """
    response = client_api.patch(f'/books/{created_book[0].id}', {'acquired': True}, format='json')

    assert response.status_code == 200
    assert models.Book.objects.values('acquired')[0].get('acquired')


def test_detail_book_page_delete(client_api, created_book):
    """
    Test to check if user can delete book
    """
    assert models.Book.objects.count() == 2

    response = client_api.delete(f'/books/{created_book[0].id}', {}, format='json')
    assert response.status_code == 204
    assert models.Book.objects.count() == 1


def test_filter_by_author(client_api, created_book):
    """
    Test to check if user can filter list of books by author
    """
    response1 = client_api.get('/books/?author=J.R.R Tolkien', {}, format='json')
    assert response1.status_code == 200
    assert len(response1.data) == 1
    assert response1.data[0]['authors'] == ['J.R.R Tolkien']

    response2 = client_api.get('/books/?author=C.S Lewis', {}, format='json')
    assert response2.status_code == 200
    assert len(response2.data) == 1
    assert response2.data[0]['authors'] == ['C.S Lewis']


def test_filter_by_date(client_api, created_book):
    """
    Test to check if user can filter list of books by specify range of date
    """
    response1 = client_api.get('/books/?from=2000&to=2002', {}, format='json')
    assert len(response1.data) == 1
    assert response1.data[0]['published_year'] == '2001'


def test_filter_by_status(client_api, created_book):
    """
    Test to check if user can filter list of books by acquired status
    """
    response = client_api.get('/books/?acquired=true', {}, format='json')
    assert len(response.data) == 1
    assert response.data[0]['acquired']


def test_filter_by_title(client_api, created_book):
    """
    Test to check if user can filter list of books by title
    """
    response = client_api.get('/books/?title=hobbit', {}, format='json')
    assert len(response.data) == 1
    assert response.data[0]['title'] == 'Hobbit'
