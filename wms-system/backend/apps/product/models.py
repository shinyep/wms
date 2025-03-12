from django.db import models
from django.utils.translation import gettext_lazy as _


class Category(models.Model):
    """商品分类模型"""
    name = models.CharField(_('分类名称'), max_length=100)
    code = models.CharField(_('分类编码'), max_length=50, unique=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, 
                              related_name='children', verbose_name=_('父分类'))
    level = models.PositiveIntegerField(_('层级'), default=1)
    is_active = models.BooleanField(_('是否启用'), default=True)
    description = models.TextField(_('描述'), blank=True, null=True)
    created_time = models.DateTimeField(_('创建时间'), auto_now_add=True)
    updated_time = models.DateTimeField(_('更新时间'), auto_now=True)

    class Meta:
        verbose_name = _('商品分类')
        verbose_name_plural = verbose_name
        ordering = ['code']

    def __str__(self):
        return self.name


class Unit(models.Model):
    """计量单位模型"""
    name = models.CharField(_('单位名称'), max_length=50)
    code = models.CharField(_('单位编码'), max_length=20, unique=True)
    description = models.TextField(_('描述'), blank=True, null=True)

    class Meta:
        verbose_name = _('计量单位')
        verbose_name_plural = verbose_name
        ordering = ['code']

    def __str__(self):
        return self.name


class Supplier(models.Model):
    """供应商模型"""
    name = models.CharField(_('供应商名称'), max_length=100)
    code = models.CharField(_('供应商编码'), max_length=50, unique=True)
    contact_person = models.CharField(_('联系人'), max_length=50, blank=True, null=True)
    contact_phone = models.CharField(_('联系电话'), max_length=20, blank=True, null=True)
    address = models.CharField(_('地址'), max_length=200, blank=True, null=True)
    email = models.EmailField(_('邮箱'), blank=True, null=True)
    is_active = models.BooleanField(_('是否启用'), default=True)
    description = models.TextField(_('描述'), blank=True, null=True)
    created_time = models.DateTimeField(_('创建时间'), auto_now_add=True)
    updated_time = models.DateTimeField(_('更新时间'), auto_now=True)

    class Meta:
        verbose_name = _('供应商')
        verbose_name_plural = verbose_name
        ordering = ['code']

    def __str__(self):
        return self.name


class Product(models.Model):
    """商品模型"""
    name = models.CharField(_('商品名称'), max_length=100)
    code = models.CharField(_('商品编码'), max_length=50, unique=True)
    barcode = models.CharField(_('条形码'), max_length=50, blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, 
                                related_name='products', verbose_name=_('商品分类'))
    unit = models.ForeignKey(Unit, on_delete=models.SET_NULL, null=True, blank=True, 
                            verbose_name=_('计量单位'))
    spec = models.CharField(_('规格'), max_length=100, blank=True, null=True)
    price = models.DecimalField(_('价格'), max_digits=10, decimal_places=2, default=0)
    cost = models.DecimalField(_('成本'), max_digits=10, decimal_places=2, default=0)
    weight = models.DecimalField(_('重量(kg)'), max_digits=10, decimal_places=2, blank=True, null=True)
    volume = models.DecimalField(_('体积(m³)'), max_digits=10, decimal_places=3, blank=True, null=True)
    min_stock = models.DecimalField(_('最小库存'), max_digits=10, decimal_places=2, default=0)
    max_stock = models.DecimalField(_('最大库存'), max_digits=10, decimal_places=2, blank=True, null=True)
    shelf_life = models.PositiveIntegerField(_('保质期(天)'), blank=True, null=True)
    is_active = models.BooleanField(_('是否启用'), default=True)
    image = models.ImageField(_('商品图片'), upload_to='products/', blank=True, null=True)
    description = models.TextField(_('描述'), blank=True, null=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, blank=True, 
                                related_name='products', verbose_name=_('默认供应商'))
    created_time = models.DateTimeField(_('创建时间'), auto_now_add=True)
    updated_time = models.DateTimeField(_('更新时间'), auto_now=True)

    class Meta:
        verbose_name = _('商品')
        verbose_name_plural = verbose_name
        ordering = ['code']

    def __str__(self):
        return f"{self.name}({self.code})" 