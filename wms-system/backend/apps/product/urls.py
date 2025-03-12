from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, UnitViewSet, SupplierViewSet, ProductViewSet

router = DefaultRouter()
router.register('categories', CategoryViewSet)
router.register('units', UnitViewSet)
router.register('suppliers', SupplierViewSet)
router.register('products', ProductViewSet)

urlpatterns = [
    path('', include(router.urls)),
] 