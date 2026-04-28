from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .serializers import ProductSerializer, CustomerSerializer, InvoiceSerializer
from .models import Product, Customer, Invoice

class ProductView(generics.ListCreateAPIView):
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Product.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CustomerView(generics.ListCreateAPIView):
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Customer.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class InvoiceView(generics.ListCreateAPIView):
    serializer_class = InvoiceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Invoice.objects.filter(user=self.request.user)
