from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q

from .models import Book, Category, ISBN
from .forms import (
    BookForm, CategoryForm, ISBNUpdateForm,
    SignUpForm, LoginForm, BookFilterForm,
)


# ── Authentication ───────────────────────────────────────────────────────────

def signup_view(request):
    if request.user.is_authenticated:
        return redirect('book_list')
    form = SignUpForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, f"Welcome, {user.username}! Your account has been created.")
        return redirect('book_list')
    return render(request, 'bookstore/signup.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('book_list')
    form = LoginForm(request, data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.get_user()
        login(request, user)
        messages.success(request, f"Welcome back, {user.username}!")
        next_url = request.GET.get('next', 'book_list')
        return redirect(next_url)
    return render(request, 'bookstore/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('login')


# ── Public views ──────────────────────────────────────────────────────────────

def book_list(request):
    """Public view: list & filter books."""
    books = Book.objects.select_related('owner', 'isbn').prefetch_related('categories').all()
    filter_form = BookFilterForm(request.GET or None)

    if filter_form.is_valid():
        search = filter_form.cleaned_data.get('search')
        category = filter_form.cleaned_data.get('category')
        owner = filter_form.cleaned_data.get('owner')
        min_price = filter_form.cleaned_data.get('min_price')
        max_price = filter_form.cleaned_data.get('max_price')

        if search:
            books = books.filter(
                Q(title__icontains=search) | Q(description__icontains=search)
            )
        if category:
            books = books.filter(categories=category)
        if owner:
            books = books.filter(owner=owner)
        if min_price is not None:
            books = books.filter(price__gte=min_price)
        if max_price is not None:
            books = books.filter(price__lte=max_price)

    return render(request, 'bookstore/book_list.html', {
        'books': books,
        'filter_form': filter_form,
        'total': books.count(),
    })


def book_detail(request, pk):
    """Public view: individual book details."""
    book = get_object_or_404(
        Book.objects.select_related('owner', 'isbn').prefetch_related('categories'),
        pk=pk
    )
    return render(request, 'bookstore/book_detail.html', {'book': book})


def category_list(request):
    """Public view: all categories."""
    categories = Category.objects.prefetch_related('books').all()
    return render(request, 'bookstore/category_list.html', {'categories': categories})


# ── Login-required views ──────────────────────────────────────────────────────

@login_required
def my_books(request):
    """Requires login: shows only the current user's books."""
    books = Book.objects.filter(owner=request.user).prefetch_related('categories').select_related('isbn')
    return render(request, 'bookstore/my_books.html', {'books': books})


@login_required
def book_create(request):
    """Requires login: create a new book."""
    form = BookForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        book = form.save()
        messages.success(request, f'Book "{book.title}" created! ISBN has been auto-generated.')
        return redirect('book_detail', pk=book.pk)
    return render(request, 'bookstore/book_form.html', {
        'form': form,
        'action': 'Create',
    })


@login_required
def book_edit(request, pk):
    """Requires login: edit a book (owner or staff only)."""
    book = get_object_or_404(Book, pk=pk)
    if book.owner != request.user and not request.user.is_staff:
        messages.error(request, "You don't have permission to edit this book.")
        return redirect('book_detail', pk=pk)

    form = BookForm(request.POST or None, instance=book)
    if request.method == 'POST' and form.is_valid():
        book = form.save()
        messages.success(request, f'Book "{book.title}" updated.')
        return redirect('book_detail', pk=book.pk)
    return render(request, 'bookstore/book_form.html', {
        'form': form,
        'action': 'Edit',
        'book': book,
    })


@login_required
def book_delete(request, pk):
    """Requires login: delete a book (owner or staff only)."""
    book = get_object_or_404(Book, pk=pk)
    if book.owner != request.user and not request.user.is_staff:
        messages.error(request, "You don't have permission to delete this book.")
        return redirect('book_detail', pk=pk)

    if request.method == 'POST':
        title = book.title
        book.delete()
        messages.success(request, f'Book "{title}" deleted.')
        return redirect('book_list')
    return render(request, 'bookstore/book_confirm_delete.html', {'book': book})


# ── Permission-required views ─────────────────────────────────────────────────

@permission_required('bookstore.add_category', raise_exception=True)
def category_create(request):
    """Requires 'bookstore.add_category' permission."""
    form = CategoryForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        cat = form.save()
        messages.success(request, f'Category "{cat.name}" created.')
        return redirect('category_list')
    return render(request, 'bookstore/category_form.html', {
        'form': form,
        'action': 'Create',
    })


@permission_required('bookstore.change_category', raise_exception=True)
def category_edit(request, pk):
    """Requires 'bookstore.change_category' permission."""
    category = get_object_or_404(Category, pk=pk)
    form = CategoryForm(request.POST or None, instance=category)
    if request.method == 'POST' and form.is_valid():
        category = form.save()
        messages.success(request, f'Category "{category.name}" updated.')
        return redirect('category_list')
    return render(request, 'bookstore/category_form.html', {
        'form': form,
        'action': 'Edit',
        'category': category,
    })


@permission_required('bookstore.delete_category', raise_exception=True)
def category_delete(request, pk):
    """Requires 'bookstore.delete_category' permission."""
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        name = category.name
        category.delete()
        messages.success(request, f'Category "{name}" deleted.')
        return redirect('category_list')
    return render(request, 'bookstore/category_confirm_delete.html', {'category': category})


@login_required
def isbn_update(request, book_pk):
    """Requires login: update ISBN metadata for a book."""
    book = get_object_or_404(Book, pk=book_pk)
    isbn = get_object_or_404(ISBN, book=book)

    if book.owner != request.user and not request.user.is_staff:
        messages.error(request, "You don't have permission to edit this ISBN.")
        return redirect('book_detail', pk=book_pk)

    form = ISBNUpdateForm(request.POST or None, instance=isbn)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "ISBN details updated.")
        return redirect('book_detail', pk=book_pk)
    return render(request, 'bookstore/isbn_form.html', {
        'form': form,
        'book': book,
        'isbn': isbn,
    })
