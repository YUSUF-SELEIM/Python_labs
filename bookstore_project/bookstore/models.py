import uuid
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator, MaxLengthValidator, MinValueValidator


class Category(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
        validators=[MinLengthValidator(2, "Category name must be at least 2 characters long.")]
    )
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(
        max_length=50,
        validators=[
            MinLengthValidator(10, "Book title must be at least 10 characters long."),
            MaxLengthValidator(50, "Book title must not exceed 50 characters."),
        ]
    )
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(0)])
    published_date = models.DateField(null=True, blank=True)
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='books',
        verbose_name="Owner (User)"
    )
    categories = models.ManyToManyField(
        Category,
        related_name='books',
        verbose_name="Categories"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def clean(self):
        from django.core.exceptions import ValidationError
        if self.title:
            if len(self.title) < 10:
                raise ValidationError({'title': 'Book title must be at least 10 characters long.'})
            if len(self.title) > 50:
                raise ValidationError({'title': 'Book title must not exceed 50 characters.'})


class ISBN(models.Model):
    book = models.OneToOneField(
        Book,
        on_delete=models.CASCADE,
        related_name='isbn'
    )
    isbn_number = models.CharField(
        max_length=17,
        unique=True,
        editable=False,
        help_text="Auto-generated ISBN-13 number"
    )
    author_title = models.CharField(
        max_length=200,
        verbose_name="Author Title / Name",
        help_text="e.g., Dr., Prof., Mr., Ms. + full name"
    )
    book_title = models.CharField(
        max_length=200,
        verbose_name="Book Title (on ISBN)",
        help_text="Official title as it appears on the ISBN record"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "ISBN"
        verbose_name_plural = "ISBNs"

    def save(self, *args, **kwargs):
        if not self.isbn_number:
            self.isbn_number = self._generate_isbn()
        super().save(*args, **kwargs)

    def _generate_isbn(self):
        """Generate a valid ISBN-13 number."""
        prefix = "978"
        unique_part = str(uuid.uuid4().int)[:9]
        raw = prefix + unique_part
        # Calculate check digit
        total = sum(
            int(d) * (1 if i % 2 == 0 else 3)
            for i, d in enumerate(raw)
        )
        check = (10 - (total % 10)) % 10
        isbn_digits = raw + str(check)
        # Format as 978-X-XX-XXXXXX-X
        return f"{isbn_digits[0:3]}-{isbn_digits[3]}-{isbn_digits[4:6]}-{isbn_digits[6:12]}-{isbn_digits[12]}"

    def __str__(self):
        return f"ISBN {self.isbn_number} — {self.book_title}"
