from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.warehouse.models import Warehouse
from apps.product.models import Product, Supplier
from apps.user.models import User


class Customer(models.Model):
    """客户模型"""
    name = models.CharField(_('客户名称'), max_length=100)
    code = models.CharField(_('客户编码'), max_length=50, unique=True)
    contact_person = models.CharField(_('联系人'), max_length=50, blank=True, null=True)
    contact_phone = models.CharField(_('联系电话'), max_length=20, blank=True, null=True)
    address = models.CharField(_('地址'), max_length=200, blank=True, null=True)
    email = models.EmailField(_('邮箱'), blank=True, null=True)
    is_active = models.BooleanField(_('是否启用'), default=True)
    description = models.TextField(_('描述'), blank=True, null=True)
    created_time = models.DateTimeField(_('创建时间'), auto_now_add=True)
    updated_time = models.DateTimeField(_('更新时间'), auto_now=True)

    class Meta:
        verbose_name = _('客户')
        verbose_name_plural = verbose_name
        ordering = ['code']

    def __str__(self):
        return self.name


class Order(models.Model):
    """订单模型"""
    ORDER_TYPE_CHOICES = [
        ('inbound', '入库单'),
        ('outbound', '出库单'),
        ('transfer', '调拨单'),
        ('return', '退货单'),
    ]
    
    STATUS_CHOICES = [
        ('draft', '草稿'),
        ('confirmed', '已确认'),
        ('processing', '处理中'),
        ('completed', '已完成'),
        ('cancelled', '已取消'),
    ]
    
    order_code = models.CharField(_('订单编号'), max_length=50, unique=True)
    order_type = models.CharField(_('订单类型'), max_length=20, choices=ORDER_TYPE_CHOICES)
    status = models.CharField(_('状态'), max_length=20, choices=STATUS_CHOICES, default='draft')
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name='orders', 
                                 verbose_name=_('仓库'))
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True, 
                                related_name='orders', verbose_name=_('客户'))
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, blank=True, 
                                related_name='orders', verbose_name=_('供应商'))
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, 
                               related_name='created_orders', verbose_name=_('创建人'))
    handler = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, 
                               related_name='handled_orders', verbose_name=_('处理人'))
    total_amount = models.DecimalField(_('总金额'), max_digits=12, decimal_places=2, default=0)
    order_date = models.DateField(_('订单日期'))
    expected_date = models.DateField(_('预计日期'), blank=True, null=True)
    completion_date = models.DateField(_('完成日期'), blank=True, null=True)
    remark = models.TextField(_('备注'), blank=True, null=True)
    created_time = models.DateTimeField(_('创建时间'), auto_now_add=True)
    updated_time = models.DateTimeField(_('更新时间'), auto_now=True)

    class Meta:
        verbose_name = _('订单')
        verbose_name_plural = verbose_name
        ordering = ['-created_time']

    def __str__(self):
        return f"{self.order_code} - {self.get_order_type_display()}"


class OrderItem(models.Model):
    """订单明细模型"""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', 
                             verbose_name=_('订单'))
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_items', 
                               verbose_name=_('商品'))
    quantity = models.DecimalField(_('数量'), max_digits=10, decimal_places=2)
    unit_price = models.DecimalField(_('单价'), max_digits=10, decimal_places=2, default=0)
    total_price = models.DecimalField(_('总价'), max_digits=12, decimal_places=2, default=0)
    batch_number = models.CharField(_('批次号'), max_length=50, blank=True, null=True)
    production_date = models.DateField(_('生产日期'), blank=True, null=True)
    expiry_date = models.DateField(_('过期日期'), blank=True, null=True)
    processed_quantity = models.DecimalField(_('已处理数量'), max_digits=10, decimal_places=2, default=0)
    status = models.CharField(_('状态'), max_length=20, 
                             choices=[('pending', '待处理'), ('partial', '部分处理'), ('completed', '已完成')])
    remark = models.TextField(_('备注'), blank=True, null=True)

    class Meta:
        verbose_name = _('订单明细')
        verbose_name_plural = verbose_name
        ordering = ['order', 'id']

    def __str__(self):
        return f"{self.order.order_code} - {self.product.name} - {self.quantity}"


class OrderLog(models.Model):
    """订单日志模型"""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='logs', 
                             verbose_name=_('订单'))
    action = models.CharField(_('操作'), max_length=50)
    status_before = models.CharField(_('操作前状态'), max_length=20, blank=True, null=True)
    status_after = models.CharField(_('操作后状态'), max_length=20, blank=True, null=True)
    operator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, 
                                related_name='order_logs', verbose_name=_('操作人'))
    operation_time = models.DateTimeField(_('操作时间'), auto_now_add=True)
    remark = models.TextField(_('备注'), blank=True, null=True)

    class Meta:
        verbose_name = _('订单日志')
        verbose_name_plural = verbose_name
        ordering = ['-operation_time']

    def __str__(self):
        return f"{self.order.order_code} - {self.action}" 