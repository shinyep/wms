from rest_framework import serializers
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from .models import User


class UserSerializer(serializers.ModelSerializer):
    """用户序列化器"""
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'role', 
                 'phone', 'avatar', 'department', 'position', 'is_active', 'date_joined', 'level']
        read_only_fields = ['date_joined']


class UserCreateSerializer(serializers.ModelSerializer):
    """用户创建序列化器"""
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    confirm_password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'confirm_password', 'first_name', 'last_name', 
                 'role', 'phone', 'avatar', 'department', 'position', 'is_active', 'level']

    def validate(self, attrs):
        if attrs['password'] != attrs.pop('confirm_password'):
            raise serializers.ValidationError({'confirm_password': _('两次密码不一致')})
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            role=validated_data.get('role', 'viewer'),
            phone=validated_data.get('phone', ''),
            department=validated_data.get('department', ''),
            position=validated_data.get('position', ''),
            is_active=validated_data.get('is_active', True),
            level=validated_data.get('level', 1),
        )
        if 'avatar' in validated_data:
            user.avatar = validated_data['avatar']
            user.save()
        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    """用户更新序列化器"""
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'role', 'phone', 
                 'avatar', 'department', 'position', 'is_active', 'level']


class PasswordChangeSerializer(serializers.Serializer):
    """密码修改序列化器"""
    old_password = serializers.CharField(required=True, style={'input_type': 'password'})
    new_password = serializers.CharField(required=True, style={'input_type': 'password'})
    confirm_password = serializers.CharField(required=True, style={'input_type': 'password'})

    def validate(self, attrs):
        if attrs['new_password'] != attrs['confirm_password']:
            raise serializers.ValidationError({'confirm_password': _('两次密码不一致')})
        return attrs


class LoginSerializer(serializers.Serializer):
    """登录序列化器"""
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, style={'input_type': 'password'})

    def validate(self, attrs):
        # 使用Django的authenticate函数进行认证
        try:
            user = authenticate(username=attrs['username'], password=attrs['password'])
            if not user:
                # 使用字典形式的错误消息
                raise serializers.ValidationError({'non_field_errors': [_('用户名或密码错误')]})
            if not user.is_active:
                # 使用字典形式的错误消息
                raise serializers.ValidationError({'non_field_errors': [_('用户已被禁用')]})
            attrs['user'] = user
            return attrs
        except Exception as e:
            print(f"登录验证异常: {str(e)}")
            # 通用错误消息，使用字典形式
            raise serializers.ValidationError({'non_field_errors': [_('用户名或密码错误')]})


class RegisterSerializer(serializers.ModelSerializer):
    """用户注册序列化器"""
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    confirm_password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'confirm_password', 'first_name', 'last_name', 'phone']

    def validate(self, attrs):
        if attrs['password'] != attrs.pop('confirm_password'):
            raise serializers.ValidationError({'confirm_password': _('两次密码不一致')})
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            phone=validated_data.get('phone', ''),
            role='viewer',
            is_active=True,
            level=1,
        )
        return user


class UserLevelSerializer(serializers.ModelSerializer):
    """用户等级序列化器"""
    class Meta:
        model = User
        fields = ['id', 'username', 'level']
        read_only_fields = ['id', 'username'] 