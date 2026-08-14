from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from django.utils import timezone
from .models import Book, BookCopy, Member, BorrowRecord
from .serializers import (
    BookSerializer, BookCopySerializer,
    MemberSerializer, BorrowRecordSerializer
)

# ── BOOKS ──────────────────────────────────────────

@api_view(['GET'])
def book_list(request):
    books = Book.objects.all()
    search = request.query_params.get('search', None)
    if search:
        books = books.filter(title__icontains=search) | \
                books.filter(author__icontains=search) | \
                books.filter(isbn__icontains=search)
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
        book = serializer.save()
        # Auto create first copy
        BookCopy.objects.create(book=book, copy_number='001', status='available')
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT'])
def book_detail(request, pk):
    try:
        book = Book.objects.get(pk=pk)
    except Book.DoesNotExist:
        return Response({'error': 'Book not found'}, status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = BookSerializer(book)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = BookSerializer(book, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ── BOOK COPIES ─────────────────────────────────────

@api_view(['GET', 'POST'])
def book_copies(request, book_id):
    try:
        book = Book.objects.get(pk=book_id)
    except Book.DoesNotExist:
        return Response({'error': 'Book not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        copies = BookCopy.objects.filter(book=book)
        serializer = BookCopySerializer(copies, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        data = request.data.copy()
        data['book'] = book_id
        serializer = BookCopySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ── MEMBERS ─────────────────────────────────────────

@api_view(['GET'])
def member_list(request):
    members = Member.objects.all()
    search = request.query_params.get('search', None)
    if search:
        members = members.filter(name__icontains=search) | \
                  members.filter(email__icontains=search)
    status_filter = request.query_params.get('status', 'all')
    if status_filter == 'active':
        members = members.filter(is_active=True)
    elif status_filter == 'inactive':
        members = members.filter(is_active=False)
    members = members.order_by('-created_at')
    serializer = MemberSerializer(members, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def member_create(request):
    serializer = MemberSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT'])
def member_detail(request, pk):
    try:
        member = Member.objects.get(pk=pk)
    except Member.DoesNotExist:
        return Response({'error': 'Member not found'}, status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = MemberSerializer(member)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = MemberSerializer(member, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ── BORROW & RETURN ─────────────────────────────────

@api_view(['POST'])
def borrow_book(request):
    member_id = request.data.get('member_id')
    copy_id = request.data.get('copy_id')

    try:
        member = Member.objects.get(pk=member_id)
    except Member.DoesNotExist:
        return Response({'error': 'Member not found'}, status=status.HTTP_404_NOT_FOUND)

    if not member.is_active:
        return Response({'error': 'Inactive members cannot borrow books'},
                        status=status.HTTP_400_BAD_REQUEST)

    try:
        # Use select_for_update to prevent concurrent borrowing
        with transaction.atomic():
            copy = BookCopy.objects.select_for_update().get(pk=copy_id)
            if copy.status != 'available':
                return Response({'error': 'This copy is not available for borrowing'},
                                status=status.HTTP_400_BAD_REQUEST)
            copy.status = 'borrowed'
            copy.save()
            record = BorrowRecord.objects.create(
                member=member,
                book_copy=copy,
            )
            serializer = BorrowRecordSerializer(record)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    except BookCopy.DoesNotExist:
        return Response({'error': 'Book copy not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def return_book(request, record_id):
    try:
        record = BorrowRecord.objects.get(pk=record_id, is_returned=False)
    except BorrowRecord.DoesNotExist:
        return Response({'error': 'Active borrow record not found'},
                        status=status.HTTP_404_NOT_FOUND)

    with transaction.atomic():
        record.is_returned = True
        record.returned_at = timezone.now()
        record.save()
        copy = record.book_copy
        copy.status = 'available'
        copy.save()

    serializer = BorrowRecordSerializer(record)
    return Response(serializer.data)

@api_view(['GET'])
def borrow_history(request):
    records = BorrowRecord.objects.all().order_by('-borrowed_at')
    member_id = request.query_params.get('member_id')
    if member_id:
        records = records.filter(member_id=member_id)
    serializer = BorrowRecordSerializer(records, many=True)
    return Response(serializer.data)