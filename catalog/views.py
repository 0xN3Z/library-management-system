"""Catalog app views — a simple home page listing all books."""

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .models import Book


@login_required
def home(request):
    """List every book in the catalog so a member can browse and borrow."""
    books = Book.objects.order_by("title")
    return render(request, "catalog/home.html", {"books": books})
