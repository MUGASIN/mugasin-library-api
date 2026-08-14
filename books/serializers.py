from rest_framework import serializers
from .models import Book
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
        # Duplicate check: same title + author
        title = data.get('title', '').strip().lower()
        author = data.get('author', '').strip().lower()
        isbn = data.get('isbn', '').strip()

        instance = self.instance  # None on create, Book object on update

        # Check duplicate ISBN
        isbn_qs = Book.objects.filter(isbn__iexact=isbn)
        if instance:
            isbn_qs = isbn_qs.exclude(pk=instance.pk)
        if isbn_qs.exists():
            raise serializers.ValidationError(
                {'isbn': 'A book with this ISBN already exists.'}
            )

        # Check duplicate title + author combination
        dup_qs = Book.objects.filter(
            title__iexact=title,
            author__iexact=author
        )
        if instance:
            dup_qs = dup_qs.exclude(pk=instance.pk)
        if dup_qs.exists():
            raise serializers.ValidationError(
                'A book with the same title and author already exists.'
            )

        return data