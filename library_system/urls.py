"""
URL configuration for library_system project.

Routes the admin, authentication (login/logout), the loans module and a
simple home page that lists books. The `loans` URLs are mounted under the
`loans/` prefix, so e.g. `my_loans` resolves to `/loans/my-loans/`.
"""

from django.contrib import admin
from django.urls import include, path

from catalog import views as catalog_views

urlpatterns = [
    path("admin/", admin.site.urls),
    # Django's built-in authentication views/URLs (login, logout, etc.)
    path("accounts/", include("django.contrib.auth.urls")),
    # Borrowing & Returning module (Member 3 Role)
    path("loans/", include("loans.urls")),
    # Simple home page that lists the catalog
    path("", catalog_views.home, name="home"),
]
