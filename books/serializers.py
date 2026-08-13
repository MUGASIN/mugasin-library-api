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