from rest_framework import serializers
from .models import Book, BookCopy, Member, BorrowRecord
import datetime

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

    def validate_title(self, value):
        if not value.strip():
            raise serializers.ValidationError("Title is required.")
        return value

    def validate_author(self, value):
        if not value.strip():
            raise serializers.ValidationError("Author is required.")
        return value

    def validate_isbn(self, value):
        if not value.strip():
            raise serializers.ValidationError("ISBN is required.")
        return value

    def validate_publication_year(self, value):
        current_year = datetime.date.today().year
        if value < 1000 or value > current_year:
            raise serializers.ValidationError(
                f"Publication year must be between 1000 and {current_year}."
            )
        return value

    def validate(self, data):
        title = data.get('title', '').strip().lower()
        author = data.get('author', '').strip().lower()
        isbn = data.get('isbn', '').strip()
        instance = self.instance

        isbn_qs = Book.objects.filter(isbn__iexact=isbn)
        if instance:
            isbn_qs = isbn_qs.exclude(pk=instance.pk)
        if isbn_qs.exists():
            raise serializers.ValidationError({'isbn': 'A book with this ISBN already exists.'})

        dup_qs = Book.objects.filter(title__iexact=title, author__iexact=author)
        if instance:
            dup_qs = dup_qs.exclude(pk=instance.pk)
        if dup_qs.exists():
            raise serializers.ValidationError('A book with the same title and author already exists.')

        return data


class BookCopySerializer(serializers.ModelSerializer):
    book_title = serializers.CharField(source='book.title', read_only=True)
    book_author = serializers.CharField(source='book.author', read_only=True)

    class Meta:
        model = BookCopy
        fields = '__all__'


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = '__all__'

    def validate_name(self, value):
        if not value.strip():
            raise serializers.ValidationError("Name is required.")
        return value

    def validate_email(self, value):
        if not value.strip():
            raise serializers.ValidationError("Email is required.")
        return value


class BorrowRecordSerializer(serializers.ModelSerializer):
    member_name = serializers.CharField(source='member.name', read_only=True)
    book_title = serializers.CharField(source='book_copy.book.title', read_only=True)
    copy_number = serializers.CharField(source='book_copy.copy_number', read_only=True)

    class Meta:
        model = BorrowRecord
        fields = '__all__'