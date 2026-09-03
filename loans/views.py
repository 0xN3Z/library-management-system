"""
Loans app views - the core Borrowing & Returning business logic.

All write operations are wrapped in `transaction.atomic` blocks and lock the
affected `Book` row with `select_for_update()` so that concurrent requests
cannot both observe the same `available_copies` count before either of them
decrements it (race-condition mitigation). Prompts and outcomes are surfaced
to the user through `django.contrib.messages`.
"""

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from catalog.models import Book

from .models import Loan


@login_required
def borrow_book(request, book_id):
    """
    Let the current member borrow a book.

    Validations performed (inside a single atomic transaction):
      1. Reject a duplicate active loan for the same book & member.
      2. Reject borrowing when no physical copies are available.
    If both pass, a Loan is created and the book's available-copy count is
    decremented.
    """
    if request.method != "POST":
        messages.error(request, "Invalid request.")
        return redirect("home")

    book = get_object_or_404(Book, pk=book_id)

    # Run the whole borrow operation atomically. select_for_update() locks the
    # Book row for the duration of the transaction, preventing two concurrent
    # borrows from both passing the availability check.
    with transaction.atomic():
        locked_book = Book.objects.select_for_update().get(pk=book.pk)

        # Validation 1 - no duplicate active loans for this book & member.
        has_active_loan = Loan.objects.filter(
            member=request.user,
            book=locked_book,
            status=Loan.Status.BORROWED,
        ).exists()
        if has_active_loan:
            messages.error(request, "You already have an active loan for this book.")
            return redirect("loans:my_loans")

        # Validation 2 - at least one physical copy must be available.
        if locked_book.available_copies <= 0:
            messages.error(request, "No copies available for this book.")
            return redirect("loans:my_loans")

        # Create the loan record and decrement the available copy count.
        Loan.objects.create(member=request.user, book=locked_book)
        locked_book.available_copies -= 1
        locked_book.save(update_fields=["available_copies"])

    messages.success(request, "Book borrowed successfully!")
    return redirect("loans:my_loans")


@login_required
def return_book(request, loan_id):
    """
    Let the current member return one of their actively-borrowed books.

    Only loans belonging to the requesting member AND still in the 'borrowed'
    state can be returned, which also makes double-returns impossible.
    """
    if request.method != "POST":
        messages.error(request, "Invalid request.")
        return redirect("loans:my_loans")

    # Only the member's own, still-active loan qualifies for return. If absent
    # (wrong owner, already returned, or doesn't exist) show an error.
    loan = Loan.objects.filter(
        pk=loan_id,
        member=request.user,
        status=Loan.Status.BORROWED,
    ).first()
    if loan is None:
        messages.error(request, "Active loan not found.")
        return redirect("loans:my_loans")

    with transaction.atomic():
        # Re-lock to keep the book row update serialized with other actions.
        book = Book.objects.select_for_update().get(pk=loan.book_id)

        # Mark the loan as returned and record when it happened.
        loan.status = Loan.Status.RETURNED
        loan.return_date = timezone.now()
        loan.save(update_fields=["status", "return_date"])

        # Make the physical copy available again.
        book.available_copies += 1
        book.save(update_fields=["available_copies"])

    messages.success(request, "Book returned successfully!")
    return redirect("loans:my_loans")


@login_required
def my_loans(request):
    """
    Show the current member's loans.

    Active (still borrowed) loans are the primary focus; previously returned
    loans are supplied as a history list for convenience.
    """
    active_loans = Loan.objects.filter(
        member=request.user,
        status=Loan.Status.BORROWED,
    ).select_related("book")
    returned_loans = Loan.objects.filter(
        member=request.user,
        status=Loan.Status.RETURNED,
    ).select_related("book")

    context = {
        "active_loans": active_loans,
        "returned_loans": returned_loans,
    }
    return render(request, "loans/my_loans.html", context)