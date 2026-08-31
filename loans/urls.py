"""
Loans URL configuration.

Mounted under `/loans/` in the project URLconf.
"""

from django.urls import path

from . import views

app_name = "loans"

urlpatterns = [
    # Borrow a specific book (only via POST).
    path("borrow/<int:book_id>/", views.borrow_book, name="borrow_book"),
    # Return one of the member's active loans (only via POST).
    path("return/<int:loan_id>/", views.return_book, name="return_book"),
    # List the current member's loans.
    path("my-loans/", views.my_loans, name="my_loans"),
]
