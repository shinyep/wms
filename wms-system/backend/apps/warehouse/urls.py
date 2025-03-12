from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    WarehouseViewSet, 
    WarehouseAreaViewSet, 
    WarehouseLocationViewSet,
    ReportViewSet,
    MonthlyReportViewSet
)

# 创建路由器
router = DefaultRouter()
router.register(r'areas', WarehouseAreaViewSet, basename='area')
router.register(r'locations', WarehouseLocationViewSet, basename='location')
router.register(r'reports', ReportViewSet, basename='report')
router.register(r'monthly-report', MonthlyReportViewSet, basename='monthly-report')
router.register(r'', WarehouseViewSet, basename='warehouse')

# 自定义路由
urlpatterns = [
    path('', include(router.urls)),
] 