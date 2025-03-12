"""
URL Configuration for WMS project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# API文档配置
schema_view = get_schema_view(
    openapi.Info(
        title="WMS API",
        default_version='v1',
        description="仓库管理系统API文档",
        terms_of_service="https://www.example.com/terms/",
        contact=openapi.Contact(email="contact@example.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

# API版本
api_v1_patterns = [
    # 包含所有应用的API URLs
    path('warehouse/', include('apps.warehouse.urls')),
    path('inventory/', include('apps.inventory.urls')),
    path('product/', include('apps.product.urls')),
    path('user/', include('apps.user.urls')),
    path('order/', include('apps.order.urls')),
]

urlpatterns = [
    # 根URL重定向到Swagger文档
    path('', RedirectView.as_view(url='/swagger/', permanent=False), name='index'),
    
    path('admin/', admin.site.urls),
    
    # API文档
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    
    # API版本
    path('api/v1/', include(api_v1_patterns)),
]

# 开发环境下提供媒体文件访问
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) 