# Generated by Django 4.2.7 on 2025-03-04 03:20

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='客户名称')),
                ('code', models.CharField(max_length=50, unique=True, verbose_name='客户编码')),
                ('contact_person', models.CharField(blank=True, max_length=50, null=True, verbose_name='联系人')),
                ('contact_phone', models.CharField(blank=True, max_length=20, null=True, verbose_name='联系电话')),
                ('address', models.CharField(blank=True, max_length=200, null=True, verbose_name='地址')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='邮箱')),
                ('is_active', models.BooleanField(default=True, verbose_name='是否启用')),
                ('description', models.TextField(blank=True, null=True, verbose_name='描述')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
            ],
            options={
                'verbose_name': '客户',
                'verbose_name_plural': '客户',
                'ordering': ['code'],
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_code', models.CharField(max_length=50, unique=True, verbose_name='订单编号')),
                ('order_type', models.CharField(choices=[('inbound', '入库单'), ('outbound', '出库单'), ('transfer', '调拨单'), ('return', '退货单')], max_length=20, verbose_name='订单类型')),
                ('status', models.CharField(choices=[('draft', '草稿'), ('confirmed', '已确认'), ('processing', '处理中'), ('completed', '已完成'), ('cancelled', '已取消')], default='draft', max_length=20, verbose_name='状态')),
                ('total_amount', models.DecimalField(decimal_places=2, default=0, max_digits=12, verbose_name='总金额')),
                ('order_date', models.DateField(verbose_name='订单日期')),
                ('expected_date', models.DateField(blank=True, null=True, verbose_name='预计日期')),
                ('completion_date', models.DateField(blank=True, null=True, verbose_name='完成日期')),
                ('remark', models.TextField(blank=True, null=True, verbose_name='备注')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
            ],
            options={
                'verbose_name': '订单',
                'verbose_name_plural': '订单',
                'ordering': ['-created_time'],
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='数量')),
                ('unit_price', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='单价')),
                ('total_price', models.DecimalField(decimal_places=2, default=0, max_digits=12, verbose_name='总价')),
                ('batch_number', models.CharField(blank=True, max_length=50, null=True, verbose_name='批次号')),
                ('production_date', models.DateField(blank=True, null=True, verbose_name='生产日期')),
                ('expiry_date', models.DateField(blank=True, null=True, verbose_name='过期日期')),
                ('processed_quantity', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='已处理数量')),
                ('status', models.CharField(choices=[('pending', '待处理'), ('partial', '部分处理'), ('completed', '已完成')], max_length=20, verbose_name='状态')),
                ('remark', models.TextField(blank=True, null=True, verbose_name='备注')),
            ],
            options={
                'verbose_name': '订单明细',
                'verbose_name_plural': '订单明细',
                'ordering': ['order', 'id'],
            },
        ),
        migrations.CreateModel(
            name='OrderLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action', models.CharField(max_length=50, verbose_name='操作')),
                ('status_before', models.CharField(blank=True, max_length=20, null=True, verbose_name='操作前状态')),
                ('status_after', models.CharField(blank=True, max_length=20, null=True, verbose_name='操作后状态')),
                ('operation_time', models.DateTimeField(auto_now_add=True, verbose_name='操作时间')),
                ('remark', models.TextField(blank=True, null=True, verbose_name='备注')),
            ],
            options={
                'verbose_name': '订单日志',
                'verbose_name_plural': '订单日志',
                'ordering': ['-operation_time'],
            },
        ),
    ]
