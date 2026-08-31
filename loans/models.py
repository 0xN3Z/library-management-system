"""
Loans app - Loan model.

Models a single borrowing event: which member took which book, when, and
whether it has been returned. This is the core "Borrowing & Returning"
module used by the Member 3 role.

The app is designed to be modular and portable: member is tied to Django's
auth user model (via settings.AUTH_USER_MODEL, so no settings override is
required), and the book is imported from the catalog app.
"""

from datetime import timedelta

from django.conf import settings
from django.db import models
from django.utils import timezone

from catalog.models import Book


class Loan(models.Model):
    """A member's borrowing (and eventual return) of a single book."""

    # Standard loan period used by the `is_overdue` calculation.
    LOAN_PERIOD_DAYS = 14

    class Status(models.TextChoices):
        """Lifecycle states of a loan."""
        BORROWED = "borrowed", "Borrowed"
        RETURNED = "returned", "Returned"

    # The member who borrowed the book. Tied to the project's configured
    # auth user model rather than importing `User` directly, which keeps the
    # app portable across custom user models.
    member = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="loans",
    )
    # The book that was borrowed (from the sibling catalog app).
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name="loans",
    )
    # When the book was borrowed (set automatically on creation).
    borrow_date = models.DateTimeField(auto_now_add=True)
    # When the book was returned (None while still borrowed).
    return_date = models.DateTimeField(null=True, blank=True)
    # Current lifecycle status (borrowed or returned).
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.BORROWED,
    )

    class Meta:
        # Most recent loans first in the admin/list views.
        ordering = ["-borrow_date"]

    def __str__(self):
        return f"{self.member.username} - {self.book.title} ({self.get_status_display()})"

    @property
    def due_date(self):
        """When the book must be returned (14 days after borrowing)."""
        return self.borrow_date + timedelta(days=self.LOAN_PERIOD_DAYS)

    @property
    def is_overdue(self):
        """
        True when an active loan has exceeded the standard loan period.

        Returned loans are never overdue; only a loan still in the
        'borrowed' state whose due date has passed counts as overdue.
        """
        if self.status != self.Status.BORROWED:
            return False
        return timezone.now() > self.due_date
