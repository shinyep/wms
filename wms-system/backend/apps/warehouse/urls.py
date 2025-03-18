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
    # 删除记录路径 - 显式指定精确的URL路径
    path('delete_record/', WarehouseViewSet.as_view({'delete': 'delete_record'}), name='delete-record'),
    path('delete-record/', WarehouseViewSet.as_view({'delete': 'delete_record'}), name='delete-record-dash'),  # 支持dash格式
    path('', include(router.urls)),
] 