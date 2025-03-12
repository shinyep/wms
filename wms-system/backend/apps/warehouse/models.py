from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.user.models import User


class Warehouse(models.Model):
    """仓库模型"""
    name = models.CharField(_('仓库名称'), max_length=100)
    code = models.CharField(_('仓库编码'), max_length=50, unique=True)
    address = models.CharField(_('地址'), max_length=200, blank=True, null=True)
    contact_person = models.CharField(_('联系人'), max_length=50, blank=True, null=True)
    contact_phone = models.CharField(_('联系电话'), max_length=20, blank=True, null=True)
    is_active = models.BooleanField(_('是否启用'), default=True)
    manager = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, 
                               related_name='managed_warehouses', verbose_name=_('仓库管理员'))
    description = models.TextField(_('描述'), blank=True, null=True)
    created_time = models.DateTimeField(_('创建时间'), auto_now_add=True)
    updated_time = models.DateTimeField(_('更新时间'), auto_now=True)

    class Meta:
        verbose_name = _('仓库')
        verbose_name_plural = verbose_name
        ordering = ['code']

    def __str__(self):
        return f"{self.name}({self.code})"


class WarehouseArea(models.Model):
    """库区模型"""
    AREA_TYPES = (
        ('normal', '普通区'),
        ('cold', '冷藏区'),
        ('dangerous', '危险品区'),
        ('valuable', '贵重品区'),
    )
    
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, 
                                related_name='areas', verbose_name=_('所属仓库'))
    name = models.CharField(_('库区名称'), max_length=100)
    code = models.CharField(_('库区编码'), max_length=50)
    area_type = models.CharField(_('库区类型'), max_length=20, choices=AREA_TYPES, default='normal')
    is_active = models.BooleanField(_('是否启用'), default=True)
    description = models.TextField(_('描述'), blank=True, null=True)
    created_time = models.DateTimeField(_('创建时间'), auto_now_add=True)
    updated_time = models.DateTimeField(_('更新时间'), auto_now=True)

    class Meta:
        verbose_name = _('库区')
        verbose_name_plural = verbose_name
        unique_together = ['warehouse', 'code']
        ordering = ['warehouse', 'code']

    def __str__(self):
        return f"{self.warehouse.name}-{self.name}({self.code})"


class WarehouseLocation(models.Model):
    """库位模型"""
    LOCATION_TYPES = (
        ('shelf', '货架'),
        ('ground', '地堆'),
        ('special', '特殊区'),
    )
    
    area = models.ForeignKey(WarehouseArea, on_delete=models.CASCADE,
                           related_name='locations', verbose_name=_('所属库区'))
    name = models.CharField(_('库位名称'), max_length=100, default='未命名库位')
    code = models.CharField(_('库位编码'), max_length=50)
    location_type = models.CharField(_('库位类型'), max_length=20, choices=LOCATION_TYPES, default='shelf')
    is_active = models.BooleanField(_('是否启用'), default=True)
    is_empty = models.BooleanField(_('是否空置'), default=True)
    description = models.TextField(_('描述'), blank=True, null=True)
    created_time = models.DateTimeField(_('创建时间'), auto_now_add=True)
    updated_time = models.DateTimeField(_('更新时间'), auto_now=True)

    class Meta:
        verbose_name = _('库位')
        verbose_name_plural = verbose_name
        unique_together = ['area', 'code']
        ordering = ['area', 'code']

    def __str__(self):
        return f"{self.area.warehouse.name}-{self.area.name}-{self.code}"


class Report(models.Model):
    """报表模型，用于存储生成的报表信息"""
    title = models.CharField(_('报表标题'), max_length=100)
    key = models.CharField(_('报表唯一标识'), max_length=100, unique=True, null=True)
    warehouse = models.ForeignKey(Warehouse, verbose_name=_('仓库'), on_delete=models.CASCADE, related_name="reports")
    report_date = models.DateField(_('报表日期'))
    description = models.TextField(_('报表描述'), blank=True, null=True)
    data = models.JSONField(_('报表数据'), default=dict)
    created_at = models.DateTimeField(_('创建时间'), auto_now_add=True)
    updated_at = models.DateTimeField(_('更新时间'), auto_now=True)
    creator = models.ForeignKey(User, verbose_name=_('创建者'), on_delete=models.SET_NULL, null=True, related_name="created_reports")
    
    class Meta:
        verbose_name = _('报表')
        verbose_name_plural = verbose_name
        ordering = ['-created_at']
        
    def __str__(self):
        return f"{self.title} - {self.warehouse.name} - {self.report_date}" 