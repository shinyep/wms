from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import InventoryViewSet, TransactionViewSet, StockCheckViewSet, StockCheckItemViewSet

router = DefaultRouter()
router.register('inventories', InventoryViewSet)
router.register('transactions', TransactionViewSet)
router.register('stock-checks', StockCheckViewSet)
router.register('stock-check-items', StockCheckItemViewSet)

urlpatterns = [
    path('', include(router.urls)),
]