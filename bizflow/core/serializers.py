from rest_framework import serializers
from .models import Product, Customer, Invoice, InvoiceItem
from django.db import transaction


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'quantity']


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'name', 'email', 'mobile']


class InvoiceItemSerializer(serializers.ModelSerializer):
    product_details = ProductSerializer(source='product', read_only=True)

    class Meta:
        model = InvoiceItem
        fields = ['product', 'product_details', 'quantity', 'price']
        read_only_fields = ['invoice', 'price']


class InvoiceSerializer(serializers.ModelSerializer):
    items = InvoiceItemSerializer(many=True)
    customer_details = CustomerSerializer(source='customer', read_only=True)

    class Meta:
        model = Invoice
        fields = [
            'id',
            'customer',
            'customer_details',
            'created_at',
            'total_amount',
            'items'
        ]
        read_only_fields = ['total_amount']
    
    def create(self, validated_data):
        items_data = validated_data.pop('items')
        user = self.context['request'].user

        total = 0

        # 🔹 First calculate total WITHOUT saving anything
        for item_data in items_data:
            product = item_data['product']
            quantity = item_data['quantity']

            if product.quantity < quantity:
                raise serializers.ValidationError(
                    f"Not enough stock for {product.name}"
                )

            total += product.price * quantity

        # 🔹 Now create everything safely
        with transaction.atomic():

            invoice = Invoice.objects.create(
                user=user,
                total_amount=total,   # ✅ FIX: pass here
                **validated_data
            )

            for item_data in items_data:
                product = item_data['product']
                quantity = item_data['quantity']

                product.quantity -= quantity
                product.save()

                InvoiceItem.objects.create(
                    invoice=invoice,
                    product=product,
                    quantity=quantity,
                    price=product.price
                )

        return invoice
