"""
Management command: python manage.py seed_data
Creates demo categories, users, and books for testing.
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType
from bookstore.models import Category, Book


class Command(BaseCommand):
    help = 'Seed the database with demo data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding demo data...')

        # Superuser
        if not User.objects.filter(username='admin').exists():
            admin = User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
            self.stdout.write(self.style.SUCCESS('  Created superuser: admin / admin123'))
        else:
            admin = User.objects.get(username='admin')

        # Staff user with category permissions
        if not User.objects.filter(username='editor').exists():
            editor = User.objects.create_user('editor', 'editor@example.com', 'editor123',
                                               first_name='Jane', last_name='Editor')
            editor.is_staff = False
            ct = ContentType.objects.get_for_model(Category)
            for codename in ['add_category', 'change_category', 'delete_category']:
                perm = Permission.objects.get(content_type=ct, codename=codename)
                editor.user_permissions.add(perm)
            editor.save()
            self.stdout.write(self.style.SUCCESS('  Created editor user: editor / editor123 (with category permissions)'))
        else:
            editor = User.objects.get(username='editor')

        # Regular user
        if not User.objects.filter(username='reader').exists():
            reader = User.objects.create_user('reader', 'reader@example.com', 'reader123',
                                               first_name='John', last_name='Reader')
            self.stdout.write(self.style.SUCCESS('  Created regular user: reader / reader123'))
        else:
            reader = User.objects.get(username='reader')

        # Categories
        categories_data = [
            ('Fiction', 'Fictional stories and narratives'),
            ('Science', 'Science and technology books'),
            ('History', 'Historical non-fiction'),
            ('Philosophy', 'Philosophical works'),
            ('Programming', 'Software development and coding'),
        ]
        categories = {}
        for name, desc in categories_data:
            cat, created = Category.objects.get_or_create(name=name, defaults={'description': desc})
            categories[name] = cat
            if created:
                self.stdout.write(f'  Created category: {name}')

        # Books
        books_data = [
            {
                'title': 'The Art of Clean Code',
                'description': 'A guide to writing clean, maintainable code that stands the test of time.',
                'price': '29.99',
                'owner': admin,
                'categories': ['Programming', 'Science'],
            },
            {
                'title': 'Django for Beginners',
                'description': 'Learn Django by building and deploying simple web apps.',
                'price': '24.99',
                'owner': editor,
                'categories': ['Programming'],
            },
            {
                'title': 'A History of Modern Science',
                'description': 'A comprehensive overview of modern scientific developments.',
                'price': '34.99',
                'owner': reader,
                'categories': ['History', 'Science'],
            },
            {
                'title': 'Introduction to Philosophy',
                'description': 'An accessible introduction to the major branches of philosophy.',
                'price': '19.99',
                'owner': admin,
                'categories': ['Philosophy'],
            },
            {
                'title': 'The Great Adventure Novel',
                'description': 'An epic tale of adventure, friendship, and discovery.',
                'price': '14.99',
                'owner': reader,
                'categories': ['Fiction'],
            },
        ]

        for data in books_data:
            if not Book.objects.filter(title=data['title']).exists():
                book = Book.objects.create(
                    title=data['title'],
                    description=data['description'],
                    price=data['price'],
                    owner=data['owner'],
                )
                for cat_name in data['categories']:
                    book.categories.add(categories[cat_name])
                self.stdout.write(self.style.SUCCESS(f'  Created book: {book.title}'))
                # Signal auto-creates ISBN

        self.stdout.write(self.style.SUCCESS('\n✅ Seeding complete!'))
        self.stdout.write('\nTest credentials:')
        self.stdout.write('  admin / admin123       → superuser + admin panel')
        self.stdout.write('  editor / editor123     → category permissions')
        self.stdout.write('  reader / reader123     → regular user')
