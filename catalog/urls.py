from django.urls import path
from . import views

urlpatterns = [
    path('catalog/', views.catalog_view, name='catalog'),
    path('my-loans/', views.my_loans_view, name='my_loans'),
]