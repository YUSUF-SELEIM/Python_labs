from django.urls import path
from . import views

urlpatterns = [
    path('categories/', views.category_list),
    path('casts/', views.cast_list),
    path('movies/', views.movie_list),
    path('movies/<int:pk>/', views.movie_detail),
]
