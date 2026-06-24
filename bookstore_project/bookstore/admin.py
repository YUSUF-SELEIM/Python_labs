from django.contrib import admin
from django.core.exceptions import ValidationError
from .models import Book, Category, ISBN


class ISBNStackedInline(admin.StackedInline):
    """
    Stacked inline for ISBN — shows full fields vertically inside the Book admin.
    Demonstrates the 'stacked model' (as opposed to TabularInline).
    """
    model = ISBN
    extra = 0
    readonly_fields = ('isbn_number', 'created_at')
    fields = ('isbn_number', 'author_title', 'book_title', 'created_at')
    can_delete = False  # ISBN is auto-created via signal; prevent orphan deletion


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    # Display columns in the list view
    list_display = ('title', 'owner', 'price', 'get_categories', 'get_isbn', 'created_at')
    list_display_links = ('title',)

    # Filters in the right sidebar
    list_filter = ('categories', 'owner', 'published_date')

    # Search fields
    search_fields = ('title', 'description', 'owner__username', 'owner__email', 'isbn__isbn_number')

    # Ordering
    ordering = ('-created_at',)

    # Inline ISBN as a stacked form
    inlines = [ISBNStackedInline]

    # Field grouping in the edit form
    fieldsets = (
        ('Book Information', {
            'fields': ('title', 'description', 'price', 'published_date'),
        }),
        ('Ownership & Classification', {
            'fields': ('owner', 'categories'),
            'description': 'Assign the book to an existing user and one or more categories.',
        }),
    )

    filter_horizontal = ('categories',)  # Nice widget for M2M

    def get_categories(self, obj):
        return ", ".join(c.name for c in obj.categories.all()) or "—"
    get_categories.short_description = "Categories"

    def get_isbn(self, obj):
        try:
            return obj.isbn.isbn_number
        except ISBN.DoesNotExist:
            return "—"
    get_isbn.short_description = "ISBN"

    def save_model(self, request, obj, form, change):
        """Run full_clean before saving to enforce model-level validators in the admin."""
        try:
            obj.full_clean()
        except ValidationError as e:
            # Re-raise so Django admin shows the error nicely
            raise ValidationError(e.message_dict)
        super().save_model(request, obj, form, change)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'book_count', 'created_at')
    search_fields = ('name',)
    ordering = ('name',)

    def book_count(self, obj):
        return obj.books.count()
    book_count.short_description = "# Books"

    def save_model(self, request, obj, form, change):
        try:
            obj.full_clean()
        except ValidationError as e:
            raise ValidationError(e.message_dict)
        super().save_model(request, obj, form, change)


@admin.register(ISBN)
class ISBNAdmin(admin.ModelAdmin):
    list_display = ('isbn_number', 'book', 'author_title', 'book_title', 'created_at')
    search_fields = ('isbn_number', 'author_title', 'book_title', 'book__title')
    list_filter = ('created_at',)
    readonly_fields = ('isbn_number', 'created_at')
    ordering = ('-created_at',)

    fieldsets = (
        ('Auto-generated', {
            'fields': ('isbn_number', 'created_at'),
            'description': 'These fields are set automatically.',
        }),
        ('ISBN Details', {
            'fields': ('book', 'author_title', 'book_title'),
        }),
    )
