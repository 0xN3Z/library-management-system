"""
Loans app - Loan model.

Models a single borrowing event: which member took which book, when, and
whether it has been returned.
"""

from datetime import timedelta

from django.conf import settings
from django.db import models
from django.utils import timezone

from catalog.models import Book


class Loan(models.Model):
    """A member's borrowing (and eventual return) of a single book."""

    LOAN_PERIOD_DAYS = 14

    class Status(models.TextChoices):
        BORROWED = "borrowed", "Borrowed"
        RETURNED = "returned", "Returned"

    member = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="loans",
    )
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name="loans",
    )
    borrow_date = models.DateTimeField(auto_now_add=True)
    return_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.BORROWED,
    )

    class Meta:
        ordering = ["-borrow_date"]

    def __str__(self):
        return f"{self.member.username} - {self.book.title} ({self.get_status_display()})"

    @property
    def due_date(self):
        """When the book must be returned (14 days after borrowing)."""
        return self.borrow_date + timedelta(days=self.LOAN_PERIOD_DAYS)

    @property
    def is_overdue(self):
        """True when an active loan has exceeded the standard loan period."""
        if self.status != self.Status.BORROWED:
            return False
        return timezone.now() > self.due_date

    @property
    def days_remaining(self):
        """
        Whole days left until the due date for an active loan.
        Returns None for returned loans. Can be negative if overdue.
        """
        if self.status != self.Status.BORROWED:
            return None
        delta = self.due_date - timezone.now()
        return delta.days

    @property
    def due_soon(self):
        """True when an active, non-overdue loan is due within 3 days."""
        if self.status != self.Status.BORROWED or self.is_overdue:
            return False
        return self.days_remaining <= 3