from .views import ProductView, CustomerView, InvoiceView
from django.urls import path

urlpatterns = [
    path('products/', ProductView.as_view()),
    path('customers/', CustomerView.as_view()),
    path('invoices/', InvoiceView.as_view()),
]
