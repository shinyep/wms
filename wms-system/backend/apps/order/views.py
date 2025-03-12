from rest_framework import viewsets
from .models import Customer, Order, OrderItem
from .serializers import CustomerSerializer, OrderSerializer, OrderItemSerializer

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    filterset_fields = ['code', 'name', 'status']
    search_fields = ['code', 'name', 'contact_person', 'contact_phone', 'address', 'email']
    ordering_fields = ['id', 'code', 'name', 'created_at']
    ordering = ['code']

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filterset_fields = ['order_code', 'order_type', 'status', 'warehouse', 'supplier', 'customer', 'creator', 'handler']
    search_fields = ['order_code', 'remark']
    ordering_fields = ['id', 'order_code', 'order_date', 'total_amount', 'created_at']
    ordering = ['-created_at']

class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    filterset_fields = ['order', 'product', 'status']
    search_fields = ['batch_number', 'product__name', 'product__code']
    ordering_fields = ['id', 'created_at']
    ordering = ['-created_at'] 