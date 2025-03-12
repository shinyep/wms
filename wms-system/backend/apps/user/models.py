from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """
    自定义用户模型
    """
    ROLE_CHOICES = (
        ('admin', '管理员'),
        ('manager', '仓库经理'),
        ('operator', '操作员'),
        ('viewer', '查看者'),
    )
    
    LEVEL_CHOICES = (
        (0, '普通用户'),
        (1, '高级用户'),
        (2, '企业用户'),
        (3, '超级管理员'),
    )
    
    role = models.CharField(_('角色'), max_length=20, choices=ROLE_CHOICES, default='viewer')
    phone = models.CharField(_('手机号'), max_length=11, blank=True, null=True)
    avatar = models.ImageField(_('头像'), upload_to='avatars/', blank=True, null=True)
    department = models.CharField(_('部门'), max_length=50, blank=True, null=True)
    position = models.CharField(_('职位'), max_length=50, blank=True, null=True)
    name = models.CharField(_('姓名'), max_length=50, blank=True)
    is_warehouse_admin = models.BooleanField(_('是否仓库管理员'), default=False)
    level = models.IntegerField(_('用户等级'), choices=LEVEL_CHOICES, default=1)
    
    class Meta:
        verbose_name = _('用户')
        verbose_name_plural = verbose_name
        ordering = ['-date_joined']
    
    def __str__(self):
        return self.username or self.name 