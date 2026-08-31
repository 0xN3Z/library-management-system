"""Catalog admin — allow librarians to manage books and their copy counts."""

from django.contrib import admin

from .models import Book


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "isbn", "category", "total_copies", "available_copies")
    list_filter = ("category",)
    search_fields = ("title", "author", "isbn")
