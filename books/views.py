from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Book
from .serializers import BookSerializer

# Create your views here.

@api_view(['GET'])
def book_list(request):
    books = Book.objects.all()

    # Search
    search = request.query_params.get('search', None)
    if search:
        books = books.filter(
            title__icontains=search
        ) | books.filter(
            author__icontains=search
        ) | books.filter(
            isbn__icontains=search
        )

    # Filter by status
    status_filter = request.query_params.get('status', 'all')
    if status_filter == 'active':
        books = books.filter(is_active=True)
    elif status_filter == 'inactive':
        books = books.filter(is_active=False)

    books = books.order_by('-created_at')
    serializer = BookSerializer(books, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def book_create(request):
    serializer = BookSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def book_detail(request, pk):
    try:
        book = Book.objects.get(pk=pk)
    except Book.DoesNotExist:
        return Response({'error': 'Book not found'}, status=status.HTTP_404_NOT_FOUND)
    serializer = BookSerializer(book)
    return Response(serializer.data)

@api_view(['PUT'])
def book_update(request, pk):
    try:
        book = Book.objects.get(pk=pk)
    except Book.DoesNotExist:
        return Response({'error': 'Book not found'}, status=status.HTTP_404_NOT_FOUND)
    serializer = BookSerializer(book, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)