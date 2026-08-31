"""
Loans admin — let librarians track who borrowed which book.

Provides a filterable, searchable list of every loan with its lifecycle
status so staff can quickly see outstanding and returned borrows.
"""

from django.contrib import admin

from .models import Loan


@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = ("member", "book", "borrow_date", "return_date", "status")
    list_filter = ("status", "borrow_date")
    search_fields = ("member__username", "member__email", "book__title", "book__isbn")
    # Load the related Member and Book in a single query for the list view.
    list_select_related = ("member", "book")
    list_per_page = 25
