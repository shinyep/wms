from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils.translation import gettext_lazy as _
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .models import User
from .serializers import (
    UserSerializer, UserCreateSerializer, UserUpdateSerializer,
    PasswordChangeSerializer, LoginSerializer, RegisterSerializer, UserLevelSerializer
)

class BasePermission(permissions.BasePermission):
    """
    基础权限类，根据用户等级（1-3级）判断权限
    1级：读写权限（不能删除）
    2级：读写权限（不能删除）
    3级：完全权限（包括删除）
    """
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
            
        user_level = request.user.level
        
        # GET请求(查看)允许所有登录用户
        if request.method in permissions.SAFE_METHODS:
            return user_level >= 1
            
        # DELETE请求需要3级权限
        if request.method == 'DELETE':
            return user_level >= 3
            
        # 其他请求(POST, PUT, PATCH)需要1级及以上权限
        return user_level >= 1

class WarehouseViewPermission(BasePermission):
    """
    仓库操作的权限控制，继承基础权限类
    特殊处理update_monthly_report方法
    """
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
            
        user_level = request.user.level
        
        # 特殊处理update_monthly_report方法，确保1级用户可以操作
        if getattr(view, 'action', None) == 'update_monthly_report':
            return user_level >= 1
        
        # 特殊处理所有写入操作，允许高级用户（Level=1）
        if request.method in ['POST', 'PUT', 'PATCH']:
            return user_level >= 1
            
        return super().has_permission(request, view)

class InventoryViewPermission(BasePermission):
    """
    库存操作的权限控制，继承基础权限类
    """
    pass

@method_decorator(csrf_exempt, name='dispatch')
class UserViewSet(viewsets.ModelViewSet):
    """用户视图集"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filterset_fields = ['username', 'is_active', 'level']
    search_fields = ['username', 'first_name', 'last_name', 'email', 'phone']
    ordering_fields = ['username', 'date_joined', 'level']
    ordering = ['-date_joined']

    def get_serializer_class(self):
        """根据不同操作返回不同的序列化器"""
        if self.action == 'login':
            return LoginSerializer
        elif self.action == 'register':
            return RegisterSerializer
        elif self.action == 'create':
            return UserCreateSerializer
        elif self.action == 'update' or self.action == 'partial_update':
            return UserUpdateSerializer
        elif self.action == 'change_password':
            return PasswordChangeSerializer
        elif self.action == 'set_user_level':
            return UserLevelSerializer
        return UserSerializer

    def get_permissions(self):
        if self.action in ['login', 'register', 'logout']:
            permission_classes = [permissions.AllowAny]
        elif self.action in ['list', 'retrieve', 'info']:
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [BasePermission]
        return [permission() for permission in permission_classes]

    @action(detail=False, methods=['get'])
    def permissions(self, request):
        """获取当前用户的权限信息"""
        user_level = request.user.level
        
        # 简化的权限信息
        permissions = {
            'level': user_level,
            'can_view': user_level >= 1,    # 1级及以上可查看
            'can_add': user_level >= 1,     # 1级及以上可新增
            'can_edit': user_level >= 1,    # 1级及以上可编辑
            'can_delete': user_level >= 3,  # 3级可删除
            'can_export': user_level >= 1,  # 1级及以上可导出
            'can_import': user_level >= 1,  # 1级及以上可导入
            'is_admin': user_level >= 3     # 3级为管理员
        }
        
        return Response(permissions)

    @action(detail=False, methods=['post'])
    def login(self, request):
        """用户登录"""
        # 添加日志记录
        print(f"登录请求: {request.data}")
        
        serializer = self.get_serializer(data=request.data)
        
        # 验证序列化器
        try:
            serializer.is_valid(raise_exception=True)
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)
            
            return Response({
                'token': str(refresh.access_token),
                'user': UserSerializer(user).data
            })
        except Exception as e:
            print(f"登录验证错误: {str(e)}")
            # 重新抛出异常，让DRF处理
            raise
    
    @action(detail=False, methods=['post'])
    def register(self, request):
        """用户注册"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'token': str(refresh.access_token),
            'user': UserSerializer(user).data
        }, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get'])
    def info(self, request):
        """获取当前用户信息"""
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def change_password(self, request, pk=None):
        """修改密码"""
        user = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # 检查旧密码
        if not user.check_password(serializer.validated_data['old_password']):
            return Response({'old_password': [_('旧密码不正确')]}, status=status.HTTP_400_BAD_REQUEST)
        
        # 设置新密码
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        return Response({'message': _('密码修改成功')})

    @action(detail=True, methods=['post'])
    def activate(self, request, pk=None):
        """激活用户"""
        user = self.get_object()
        user.is_active = True
        user.save()
        return Response({'message': _('用户已激活')})

    @action(detail=True, methods=['post'])
    def deactivate(self, request, pk=None):
        """禁用用户"""
        user = self.get_object()
        user.is_active = False
        user.save()
        return Response({'message': _('用户已禁用')})
    
    @action(detail=True, methods=['post'])
    def set_user_level(self, request, pk=None):
        """设置用户等级（仅超级管理员可操作）"""
        user = self.get_object()
        serializer = self.get_serializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        
        # 确保当前用户是超级管理员
        if request.user.level < 3:
            return Response(
                {'detail': _('您没有权限执行此操作，需要超级管理员权限')},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # 保存用户等级
        serializer.save()
        return Response({'message': _('用户等级设置成功')})

    @action(detail=False, methods=['get'])
    def logout(self, request):
        """用户登出"""
        try:
            # 获取请求头中的token
            auth_header = request.headers.get('Authorization')
            if not auth_header or not auth_header.startswith('Bearer '):
                return Response({'message': '登出成功'})
                
            token = auth_header.split(' ')[1]
            # 将access token转换为refresh token
            try:
                # 直接返回成功，因为access token不需要加入黑名单
                return Response({'message': '登出成功'})
            except Exception as e:
                # 如果token处理出现错误，仍然返回登出成功
                return Response({'message': '登出成功'})
        except Exception as e:
            # 即使发生错误，也返回登出成功
            return Response({'message': '登出成功'})

    def get_queryset(self):
        """重写queryset，添加日志"""
        print(f"获取用户列表，当前用户: {self.request.user.username}, 等级: {self.request.user.level}")
        print(f"当前请求动作: {self.action}")
        print(f"请求参数: {self.request.query_params}")
        
        # 返回所有用户
        queryset = User.objects.all()
        
        # 记录查询结果数量
        count = queryset.count()
        print(f"查询结果数量: {count}")
        
        return queryset
        
    def list(self, request, *args, **kwargs):
        """重写list方法，确保正确返回用户列表"""
        queryset = self.filter_queryset(self.get_queryset())
        
        # 添加详细日志
        print(f"过滤后结果数量: {queryset.count()}")
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
        
    def destroy(self, request, *args, **kwargs):
        """重写delete方法，增加安全检查和错误处理"""
        try:
            # 获取要删除的用户对象
            user = self.get_object()
            
            # 记录操作信息
            print(f"尝试删除用户: {user.username}, 操作者: {request.user.username}")
            
            # 安全检查：不能删除自己
            if user.id == request.user.id:
                return Response(
                    {'detail': _('不能删除当前登录的用户账号')},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # 安全检查：只能由3级用户(超级管理员)删除用户
            if request.user.level < 3:
                return Response(
                    {'detail': _('您没有权限执行此操作，需要超级管理员权限')},
                    status=status.HTTP_403_FORBIDDEN
                )
                
            # 执行删除操作
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
            
        except Exception as e:
            print(f"删除用户时发生错误: {str(e)}")
            return Response(
                {'detail': _('删除用户失败: {}').format(str(e))},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            ) 