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
                'title': 'Clean Architecture',
                'author': 'Robert C. Martin',
                'isbn': '9780134494166',
                'category': 'Programming',
                'total_copies': 2,
                'available_copies': 2,
            },
            {
                'title': 'The Clean Coder',
                'author': 'Robert C. Martin',
                'isbn': '9780137081073',
                'category': 'Programming',
                'total_copies': 2,
                'available_copies': 2,
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
                'title': 'Animal Farm',
                'author': 'George Orwell',
                'isbn': '9780451526342',
                'category': 'Fiction',
                'total_copies': 2,
                'available_copies': 2,
            },
            {
                'title': 'Homage to Catalonia',
                'author': 'George Orwell',
                'isbn': '9780156421171',
                'category': 'History',
                'total_copies': 1,
                'available_copies': 1,
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
                'title': 'Homo Deus',
                'author': 'Yuval Noah Harari',
                'isbn': '9780062464316',
                'category': 'History',
                'total_copies': 2,
                'available_copies': 2,
            },
            {
                'title': '21 Lessons for the 21st Century',
                'author': 'Yuval Noah Harari',
                'isbn': '9780525512172',
                'category': 'History',
                'total_copies': 2,
                'available_copies': 2,
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
            {
                'title': 'Go Set a Watchman',
                'author': 'Harper Lee',
                'isbn': '9780062409850',
                'category': 'Fiction',
                'total_copies': 1,
                'available_copies': 1,
            },
        ]

        for book_data in books:
            Book.objects.update_or_create(
                isbn=book_data['isbn'],
                defaults=book_data,
            )

        self.stdout.write(self.style.SUCCESS(f'{len(books)} books ready.'))