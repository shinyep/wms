from rest_framework import viewsets
from .models import Category, Unit, Supplier, Product
from .serializers import CategorySerializer, UnitSerializer, SupplierSerializer, ProductSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filterset_fields = ['code', 'name', 'level', 'parent']
    search_fields = ['code', 'name', 'description']
    ordering_fields = ['id', 'code', 'name', 'level', 'created_at']
    ordering = ['level', 'code']

class UnitViewSet(viewsets.ModelViewSet):
    queryset = Unit.objects.all()
    serializer_class = UnitSerializer
    filterset_fields = ['code', 'name']
    search_fields = ['code', 'name', 'description']
    ordering_fields = ['id', 'code', 'name', 'created_at']
    ordering = ['code']

class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    filterset_fields = ['code', 'name', 'status']
    search_fields = ['code', 'name', 'contact_person', 'contact_phone', 'address', 'email']
    ordering_fields = ['id', 'code', 'name', 'created_at']
    ordering = ['code']

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filterset_fields = ['code', 'name', 'category', 'supplier', 'status']
    search_fields = ['code', 'name', 'barcode', 'description', 'spec']
    ordering_fields = ['id', 'code', 'name', 'price', 'created_at']
    ordering = ['code'] 