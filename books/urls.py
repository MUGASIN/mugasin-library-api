from django.urls import path
from . import views

urlpatterns = [
    # Books
    path('books/', views.book_list, name='book-list'),
    path('books/create/', views.book_create, name='book-create'),
    path('books/<int:pk>/', views.book_detail, name='book-detail'),
    path('books/<int:pk>/update/', views.book_detail, name='book-detail-update'),

    # Book Copies
    path('books/<int:book_id>/copies/', views.book_copies, name='book-copies'),

    # Members
    path('members/', views.member_list, name='member-list'),
    path('members/create/', views.member_create, name='member-create'),
    path('members/<int:pk>/', views.member_detail, name='member-detail'),

    # Borrow & Return
    path('borrow/', views.borrow_book, name='borrow-book'),
    path('return/<int:record_id>/', views.return_book, name='return-book'),
    path('borrow/history/', views.borrow_history, name='borrow-history'),
]