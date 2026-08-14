from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    isbn = models.CharField(max_length=20, unique=True)
    category = models.CharField(max_length=100, blank=True, default='')
    publication_year = models.IntegerField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class BookCopy(models.Model):
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('borrowed', 'Borrowed'),
        ('damaged', 'Damaged'),
        ('inactive', 'Inactive'),
    ]
    book = models.ForeignKey(Book, on_delete=models.PROTECT, related_name='copies')
    copy_number = models.CharField(max_length=50)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('book', 'copy_number')

    def __str__(self):
        return f"{self.book.title} - Copy {self.copy_number}"


class Member(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    joined_date = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class BorrowRecord(models.Model):
    member = models.ForeignKey(Member, on_delete=models.PROTECT, related_name='borrow_records')
    book_copy = models.ForeignKey(BookCopy, on_delete=models.PROTECT, related_name='borrow_records')
    borrowed_at = models.DateTimeField(auto_now_add=True)
    returned_at = models.DateTimeField(null=True, blank=True)
    is_returned = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.member.name} - {self.book_copy}"