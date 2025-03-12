from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from .views import UserViewSet

router = DefaultRouter()
router.register('', UserViewSet, basename='user')

# 自定义路由
custom_urlpatterns = [
    path('login/', UserViewSet.as_view({'post': 'login'}), name='login'),
    path('register/', UserViewSet.as_view({'post': 'register'}), name='register'),
    path('info/', UserViewSet.as_view({'get': 'info'}), name='user-info'),
    path('permissions/', UserViewSet.as_view({'get': 'permissions'}), name='user-permissions'),
    path('logout/', UserViewSet.as_view({'get': 'logout'}), name='logout'),
    path('refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('<int:pk>/set-level/', UserViewSet.as_view({'post': 'set_user_level'}), name='set-user-level'),
]

# 合并路由
urlpatterns = custom_urlpatterns + router.urls 