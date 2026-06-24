from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Book, ISBN


@receiver(post_save, sender=Book)
def create_isbn_for_book(sender, instance, created, **kwargs):
    """
    Signal: Automatically create an ISBN object and assign it to a newly created book.
    The ISBN number is auto-generated; author_title and book_title default to
    the book owner's full name and book title respectively.
    """
    if created:
        owner = instance.owner
        full_name = owner.get_full_name() or owner.username
        ISBN.objects.create(
            book=instance,
            author_title=full_name,
            book_title=instance.title,
        )
