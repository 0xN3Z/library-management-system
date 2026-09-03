from django.shortcuts import render
from .models import Book
from django.contrib.auth.decorators import login_required

@login_required
def catalog_view(request):
    books = Book.objects.all()
    return render(request, 'catalog.html', {'books': books})

