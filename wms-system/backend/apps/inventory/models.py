from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.warehouse.models import Warehouse, WarehouseLocation
from apps.product.models import Product
from apps.user.models import User
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
import calendar
from datetime import datetime, timedelta


class Inventory(models.Model):
    """库存模型"""
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name='warehouse_inventories', 
                                 verbose_name=_('仓库'))
    location = models.ForeignKey(WarehouseLocation, on_delete=models.SET_NULL, null=True, blank=True, 
                                related_name='location_inventories', verbose_name=_('位置'))
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_inventories', 
                               verbose_name=_('品项'))
    spec = models.CharField(_('规格/型号'), max_length=100, blank=True, null=True)
    unit = models.CharField(_('单位'), max_length=20, default='个')
    initial_quantity = models.DecimalField(_('期初库存'), max_digits=10, decimal_places=2, default=0)
    total_in = models.DecimalField(_('累计入库'), max_digits=10, decimal_places=2, default=0)
    total_out = models.DecimalField(_('累计出库'), max_digits=10, decimal_places=2, default=0)
    quantity = models.DecimalField(_('库存'), max_digits=10, decimal_places=2, default=0)
    unit_price = models.DecimalField(_('单价'), max_digits=10, decimal_places=2, default=0)
    amount = models.DecimalField(_('库存金额'), max_digits=12, decimal_places=2, default=0)
    is_active = models.BooleanField(_('是否启用'), default=True)
    created_time = models.DateTimeField(_('创建时间'), auto_now_add=True)
    updated_time = models.DateTimeField(_('更新时间'), auto_now=True)

    class Meta:
        verbose_name = _('库存')
        verbose_name_plural = verbose_name
        ordering = ['-updated_time']
        unique_together = ['warehouse', 'location', 'product']

    def __str__(self):
        return f"{self.warehouse.name}-{self.product.name}({self.quantity})"

    def save(self, *args, **kwargs):
        # 自动计算金额
        self.amount = self.quantity * self.unit_price
        super().save(*args, **kwargs)


class Transaction(models.Model):
    """库存事务模型（出入库记录）"""
    TRANSACTION_TYPES = (
        ('IN', '入库'),
        ('OUT', '出库'),
    )
    
    TRANSACTION_STATUS = (
        ('pending', '待处理'),
        ('completed', '已完成'),
        ('cancelled', '已取消'),
    )
    
    transaction_code = models.CharField(_('序号'), max_length=50, unique=True)
    transaction_date = models.DateField(_('日期'), auto_now_add=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                              related_name='product_transactions', verbose_name=_('品项'))
    spec = models.CharField(_('规格/型号'), max_length=100, blank=True, null=True)
    unit = models.CharField(_('单位'), max_length=20, default='个')
    quantity = models.DecimalField(_('数量'), max_digits=10, decimal_places=2, default=0)
    unit_price = models.DecimalField(_('单价'), max_digits=10, decimal_places=2, default=0)
    amount = models.DecimalField(_('金额'), max_digits=12, decimal_places=2, default=0)
    operator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,
                               related_name='inventory_transactions', verbose_name=_('经手人'))
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, 
                                related_name='inventory_transactions', verbose_name=_('仓库'))
    transaction_type = models.CharField(_('事务类型'), max_length=10, choices=TRANSACTION_TYPES)
    status = models.CharField(_('状态'), max_length=20, choices=TRANSACTION_STATUS, default='pending')
    remark = models.TextField(_('备注'), blank=True, null=True)
    created_time = models.DateTimeField(_('创建时间'), auto_now_add=True)
    updated_time = models.DateTimeField(_('更新时间'), auto_now=True)
    
    _original_status = None
    _original_quantity = None
    _original_transaction_date = None

    class Meta:
        verbose_name = _('出入库记录')
        verbose_name_plural = verbose_name
        ordering = ['-transaction_date', '-created_time']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 保存原始状态，用于比较是否发生变化
        self._original_status = self.status
        self._original_quantity = self.quantity
        self._original_transaction_date = self.transaction_date

    def __str__(self):
        return f"{self.transaction_code}({self.get_transaction_type_display()})"

    def save(self, *args, **kwargs):
        # 自动计算金额
        self.amount = self.quantity * self.unit_price
        
        # 保存前先保存对象，以便在post_save信号中可以获取到原始值和新值
        super().save(*args, **kwargs)

# 添加信号处理器，用于在Transaction保存后处理相关报表更新
@receiver(post_save, sender=Transaction)
def update_monthly_reports_after_transaction_save(sender, instance, **kwargs):
    """
    当Transaction保存后，检查并更新相关月份的报表数据
    """
    # 只处理已完成的事务
    if instance.status != 'completed':
        return
    
    # 获取事务所属月份
    transaction_month = instance.transaction_date.strftime("%Y-%m")
    
    # 导入这里是为了避免循环导入问题
    from apps.warehouse.views import MonthlyReportViewSet
    
    # 创建视图集实例
    report_viewset = MonthlyReportViewSet()
    
    # 1. 先更新当月报表
    try:
        # 通过视图集更新当月报表
        report_viewset.update_monthly_report_for_transaction(
            warehouse_id=instance.warehouse.id,
            month=transaction_month,
            transaction=instance
        )
    except Exception as e:
        print(f"更新当月报表失败: {e}")
    
    # 2. 获取并更新后续月份的报表
    try:
        # 计算事务月份之后的所有月份
        current_date = datetime.now().date()
        transaction_date = datetime.strptime(transaction_month + "-01", "%Y-%m-%d").date()
        
        # 生成从事务发生月份到当前月份的所有月份列表
        months_to_update = []
        next_month = transaction_date.replace(day=1) + timedelta(days=32)
        next_month = next_month.replace(day=1)  # 下一个月的第一天
        
        while next_month.replace(day=1) <= current_date.replace(day=1):
            months_to_update.append(next_month.strftime("%Y-%m"))
            next_month = next_month.replace(day=1) + timedelta(days=32)
            next_month = next_month.replace(day=1)
        
        # 更新每个后续月份的期初库存
        for month in months_to_update:
            report_viewset.update_initial_inventory_for_month(
                warehouse_id=instance.warehouse.id,
                month=month
            )
    except Exception as e:
        print(f"更新后续月份报表失败: {e}")

@receiver(post_delete, sender=Transaction)
def update_monthly_reports_after_transaction_delete(sender, instance, **kwargs):
    """
    当Transaction删除后，检查并更新相关月份的报表数据
    """
    # 只处理已完成的事务
    if instance.status != 'completed':
        return
        
    # 类似于保存后的处理逻辑
    transaction_month = instance.transaction_date.strftime("%Y-%m")
    
    from apps.warehouse.views import MonthlyReportViewSet
    report_viewset = MonthlyReportViewSet()
    
    try:
        # 通过视图集更新当月报表
        report_viewset.update_monthly_report_for_transaction(
            warehouse_id=instance.warehouse.id,
            month=transaction_month,
            transaction=None,  # 传递None表示删除操作
            deleted_transaction=instance  # 传递被删除的事务
        )
        
        # 更新后续月份
        current_date = datetime.now().date()
        transaction_date = datetime.strptime(transaction_month + "-01", "%Y-%m-%d").date()
        
        # 生成后续月份列表
        months_to_update = []
        next_month = transaction_date.replace(day=1) + timedelta(days=32)
        next_month = next_month.replace(day=1)
        
        while next_month.replace(day=1) <= current_date.replace(day=1):
            months_to_update.append(next_month.strftime("%Y-%m"))
            next_month = next_month.replace(day=1) + timedelta(days=32)
            next_month = next_month.replace(day=1)
        
        # 更新每个后续月份
        for month in months_to_update:
            report_viewset.update_initial_inventory_for_month(
                warehouse_id=instance.warehouse.id,
                month=month
            )
    except Exception as e:
        print(f"删除事务后更新报表失败: {e}")

class StockCheck(models.Model):
    """库存盘点模型"""
    STATUS_CHOICES = [
        ('draft', '草稿'),
        ('in_progress', '进行中'),
        ('completed', '已完成'),
        ('cancelled', '已取消'),
    ]
    
    check_code = models.CharField(_('盘点单号'), max_length=50, unique=True)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name='stock_checks', 
                                 verbose_name=_('仓库'))
    check_type = models.CharField(_('盘点类型'), max_length=20, 
                                 choices=[('full', '全面盘点'), ('partial', '部分盘点')])
    status = models.CharField(_('状态'), max_length=20, choices=STATUS_CHOICES, default='draft')
    start_time = models.DateTimeField(_('开始时间'), blank=True, null=True)
    end_time = models.DateTimeField(_('结束时间'), blank=True, null=True)
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, 
                               related_name='created_checks', verbose_name=_('创建人'))
    checker = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, 
                               related_name='performed_checks', verbose_name=_('盘点人'))
    remark = models.TextField(_('备注'), blank=True, null=True)
    created_time = models.DateTimeField(_('创建时间'), auto_now_add=True)
    updated_time = models.DateTimeField(_('更新时间'), auto_now=True)

    class Meta:
        verbose_name = _('库存盘点')
        verbose_name_plural = verbose_name
        ordering = ['-created_time']

    def __str__(self):
        return f"{self.check_code} - {self.warehouse.name}"


class StockCheckItem(models.Model):
    """库存盘点明细模型"""
    stock_check = models.ForeignKey(StockCheck, on_delete=models.CASCADE, related_name='items', 
                                   verbose_name=_('盘点单'))
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='check_items', 
                               verbose_name=_('商品'))
    location = models.ForeignKey(WarehouseLocation, on_delete=models.SET_NULL, null=True, blank=True, 
                                related_name='check_items', verbose_name=_('库位'))
    batch_number = models.CharField(_('批次号'), max_length=50, blank=True, null=True)
    system_quantity = models.DecimalField(_('系统数量'), max_digits=10, decimal_places=2, default=0)
    actual_quantity = models.DecimalField(_('实际数量'), max_digits=10, decimal_places=2, default=0)
    difference = models.DecimalField(_('差异数量'), max_digits=10, decimal_places=2, default=0)
    status = models.CharField(_('状态'), max_length=20, 
                             choices=[('pending', '待盘点'), ('checked', '已盘点'), ('adjusted', '已调整')])
    remark = models.TextField(_('备注'), blank=True, null=True)
    check_time = models.DateTimeField(_('盘点时间'), blank=True, null=True)

    class Meta:
        verbose_name = _('盘点明细')
        verbose_name_plural = verbose_name
        ordering = ['stock_check', 'product']
        unique_together = ['stock_check', 'product', 'location', 'batch_number']

    def __str__(self):
        return f"{self.stock_check.check_code} - {self.product.name}" 