# Generated by Django 4.2.7 on 2025-03-05 07:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
        ('warehouse', '0002_remove_warehouselocation_current_capacity_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('inventory', '0002_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_code', models.CharField(max_length=50, unique=True, verbose_name='事务编号')),
                ('batch_number', models.CharField(blank=True, max_length=50, null=True, verbose_name='批次号')),
                ('transaction_type', models.CharField(choices=[('IN', '入库'), ('OUT', '出库'), ('TRANSFER', '调拨'), ('RETURN', '退货'), ('ADJUST', '调整'), ('CHECK', '盘点')], max_length=10, verbose_name='事务类型')),
                ('quantity', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='数量')),
                ('before_quantity', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='操作前数量')),
                ('after_quantity', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='操作后数量')),
                ('status', models.CharField(choices=[('pending', '待处理'), ('processing', '处理中'), ('completed', '已完成'), ('cancelled', '已取消')], default='pending', max_length=20, verbose_name='状态')),
                ('reference_code', models.CharField(blank=True, max_length=50, null=True, verbose_name='关联单号')),
                ('remark', models.TextField(blank=True, null=True, verbose_name='备注')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('location', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='location_transactions', to='warehouse.warehouselocation', verbose_name='库位')),
                ('operator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='inventory_transactions', to=settings.AUTH_USER_MODEL, verbose_name='操作人')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_transactions', to='product.product', verbose_name='商品')),
                ('warehouse', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='inventory_transactions', to='warehouse.warehouse', verbose_name='仓库')),
            ],
            options={
                'verbose_name': '库存事务',
                'verbose_name_plural': '库存事务',
                'ordering': ['-created_time'],
            },
        ),
        migrations.AddField(
            model_name='inventory',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='是否启用'),
        ),
        migrations.AlterField(
            model_name='inventory',
            name='location',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='location_inventories', to='warehouse.warehouselocation', verbose_name='库位'),
        ),
        migrations.AlterField(
            model_name='inventory',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_inventories', to='product.product', verbose_name='商品'),
        ),
        migrations.AlterField(
            model_name='inventory',
            name='warehouse',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='warehouse_inventories', to='warehouse.warehouse', verbose_name='仓库'),
        ),
        migrations.DeleteModel(
            name='InventoryTransaction',
        ),
    ]
