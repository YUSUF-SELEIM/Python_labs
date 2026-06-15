from django.urls import path
from . import views

app_name = 'books'
urlpatterns = [
    path('', views.BookListView.as_view(), name='book_list'),
    path('create/', views.BookCreateView.as_view(), name='book_create'),
    path('<int:pk>/update/', views.BookUpdateView.as_view(), name='book_update'),
    path('<int:pk>/delete/', views.BookDeleteView.as_view(), name='book_delete'),
    path('<int:pk>/', views.book_detail, name='book_detail'),
]