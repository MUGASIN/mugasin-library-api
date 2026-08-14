from django.urls import path
from . import views

urlpatterns = [
    path('books/', views.book_list, name='book-list'),
    path('books/create/', views.book_create, name='book-create'),
    path('books/<int:pk>/', views.book_detail, name='book-detail'),
    path('books/<int:pk>/update/', views.book_update, name='book-update'),
]