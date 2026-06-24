from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Book, Category, ISBN


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Category name (min 2 chars)'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def clean_name(self):
        name = self.cleaned_data.get('name', '')
        if len(name) < 2:
            raise ValidationError("Category name must be at least 2 characters long.")
        return name


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'description', 'price', 'published_date', 'owner', 'categories']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Book title (10–50 characters)',
                'minlength': '10',
                'maxlength': '50',
            }),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
            'published_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'owner': forms.Select(attrs={'class': 'form-select'}),
            'categories': forms.CheckboxSelectMultiple(),
        }
        labels = {
            'owner': 'Owner (User)',
        }

    def clean_title(self):
        title = self.cleaned_data.get('title', '')
        if len(title) < 10:
            raise ValidationError("Book title must be at least 10 characters long.")
        if len(title) > 50:
            raise ValidationError("Book title must not exceed 50 characters.")
        return title

    def clean_categories(self):
        categories = self.cleaned_data.get('categories')
        if not categories:
            raise ValidationError("Please select at least one category.")
        return categories


class ISBNUpdateForm(forms.ModelForm):
    """Allow updating the ISBN's author_title and book_title (isbn_number stays auto)."""
    class Meta:
        model = ISBN
        fields = ['author_title', 'book_title']
        widgets = {
            'author_title': forms.TextInput(attrs={'class': 'form-control'}),
            'book_title': forms.TextInput(attrs={'class': 'form-control'}),
        }


class SignUpForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email address'})
    )
    first_name = forms.CharField(
        max_length=30,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First name'})
    )
    last_name = forms.CharField(
        max_length=30,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last name'})
    )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in ['username', 'password1', 'password2']:
            self.fields[field_name].widget.attrs['class'] = 'form-control'


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['password'].widget.attrs['class'] = 'form-control'


class BookFilterForm(forms.Form):
    search = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Search by title...'}),
    )
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False,
        empty_label="All Categories",
        widget=forms.Select(attrs={'class': 'form-select'}),
    )
    owner = forms.ModelChoiceField(
        queryset=User.objects.all(),
        required=False,
        empty_label="All Owners",
        widget=forms.Select(attrs={'class': 'form-select'}),
    )
    min_price = forms.DecimalField(
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Min price', 'step': '0.01'}),
    )
    max_price = forms.DecimalField(
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Max price', 'step': '0.01'}),
    )
