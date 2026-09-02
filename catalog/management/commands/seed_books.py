from django.core.management.base import BaseCommand
from catalog.models import Book


class Command(BaseCommand):
    help = 'Adds sample books to the database'

    def handle(self, *args, **kwargs):
        books = [
            {
                'title': 'Clean Code',
                'author': 'Robert C. Martin',
                'isbn': '9780132350884',
                'category': 'Programming',
                'total_copies': 3,
                'available_copies': 3,
            },
            {
                'title': '1984',
                'author': 'George Orwell',
                'isbn': '9780451524935',
                'category': 'Fiction',
                'total_copies': 2,
                'available_copies': 2,
            },
            {
                'title': 'Sapiens',
                'author': 'Yuval Noah Harari',
                'isbn': '9780062316097',
                'category': 'History',
                'total_copies': 4,
                'available_copies': 4,
            },
            {
                'title': 'The Pragmatic Programmer',
                'author': 'David Thomas, Andrew Hunt',
                'isbn': '9780135957059',
                'category': 'Programming',
                'total_copies': 2,
                'available_copies': 2,
            },
            {
                'title': 'To Kill a Mockingbird',
                'author': 'Harper Lee',
                'isbn': '9780061120084',
                'category': 'Fiction',
                'total_copies': 3,
                'available_copies': 3,
            },
        ]

        for book_data in books:
            Book.objects.get_or_create(
                isbn=book_data['isbn'],
                defaults=book_data,
            )

        self.stdout.write(self.style.SUCCESS(f'{len(books)} books ready.'))