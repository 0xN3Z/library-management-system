"""
Catalog app — Book model.

This is the supporting model that the `loans` module depends on. Only the
fields required by the borrowing/returning flow are modelled here.
"""

from django.db import models


class Book(models.Model):
    """A physical book copy tracked by the library."""

    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    isbn = models.CharField(max_length=20, unique=True, blank=True)
    category = models.CharField(max_length=100, blank=True)
    # Total number of physical copies the library owns.
    total_copies = models.PositiveIntegerField(default=0)
    # Number of copies currently on the shelf (not on loan).
    available_copies = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["title"]
