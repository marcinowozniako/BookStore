from django.urls import path

from books import views

app_name = 'books'

urlpatterns = [
    path('', views.BookListView.as_view(), name='list'),
    path('authors/', views.AuthorView.as_view(), name='authors'),
    path('<book_id>/', views.BookDetailsView.as_view(), name='details'),
]
