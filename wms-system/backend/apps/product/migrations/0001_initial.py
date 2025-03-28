# Generated by Django 4.2.7 on 2025-03-04 03:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='分类名称')),
                ('code', models.CharField(max_length=50, unique=True, verbose_name='分类编码')),
                ('level', models.PositiveIntegerField(default=1, verbose_name='层级')),
                ('is_active', models.BooleanField(default=True, verbose_name='是否启用')),
                ('description', models.TextField(blank=True, null=True, verbose_name='描述')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='product.category', verbose_name='父分类')),
            ],
            options={
                'verbose_name': '商品分类',
                'verbose_name_plural': '商品分类',
                'ordering': ['code'],
            },
        ),
        migrations.CreateModel(
            name='Supplier',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='供应商名称')),
                ('code', models.CharField(max_length=50, unique=True, verbose_name='供应商编码')),
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
                'verbose_name': '供应商',
                'verbose_name_plural': '供应商',
                'ordering': ['code'],
            },
        ),
        migrations.CreateModel(
            name='Unit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='单位名称')),
                ('code', models.CharField(max_length=20, unique=True, verbose_name='单位编码')),
                ('description', models.TextField(blank=True, null=True, verbose_name='描述')),
            ],
            options={
                'verbose_name': '计量单位',
                'verbose_name_plural': '计量单位',
                'ordering': ['code'],
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='商品名称')),
                ('code', models.CharField(max_length=50, unique=True, verbose_name='商品编码')),
                ('barcode', models.CharField(blank=True, max_length=50, null=True, verbose_name='条形码')),
                ('spec', models.CharField(blank=True, max_length=100, null=True, verbose_name='规格')),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='价格')),
                ('cost', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='成本')),
                ('weight', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='重量(kg)')),
                ('volume', models.DecimalField(blank=True, decimal_places=3, max_digits=10, null=True, verbose_name='体积(m³)')),
                ('min_stock', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='最小库存')),
                ('max_stock', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='最大库存')),
                ('shelf_life', models.PositiveIntegerField(blank=True, null=True, verbose_name='保质期(天)')),
                ('is_active', models.BooleanField(default=True, verbose_name='是否启用')),
                ('image', models.ImageField(blank=True, null=True, upload_to='products/', verbose_name='商品图片')),
                ('description', models.TextField(blank=True, null=True, verbose_name='描述')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='products', to='product.category', verbose_name='商品分类')),
                ('supplier', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='products', to='product.supplier', verbose_name='默认供应商')),
                ('unit', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='product.unit', verbose_name='计量单位')),
            ],
            options={
                'verbose_name': '商品',
                'verbose_name_plural': '商品',
                'ordering': ['code'],
            },
        ),
    ]
