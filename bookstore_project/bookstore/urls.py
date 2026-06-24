from django.urls import path
from . import views

urlpatterns = [
    # Auth
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Books (public)
    path('', views.book_list, name='book_list'),
    path('books/<int:pk>/', views.book_detail, name='book_detail'),

    # Books (login required)
    path('my-books/', views.my_books, name='my_books'),
    path('books/create/', views.book_create, name='book_create'),
    path('books/<int:pk>/edit/', views.book_edit, name='book_edit'),
    path('books/<int:pk>/delete/', views.book_delete, name='book_delete'),

    # ISBN
    path('books/<int:book_pk>/isbn/', views.isbn_update, name='isbn_update'),

    # Categories (public list, permission-required C/U/D)
    path('categories/', views.category_list, name='category_list'),
    path('categories/create/', views.category_create, name='category_create'),
    path('categories/<int:pk>/edit/', views.category_edit, name='category_edit'),
    path('categories/<int:pk>/delete/', views.category_delete, name='category_delete'),
]
