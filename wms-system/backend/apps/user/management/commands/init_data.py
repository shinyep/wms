import os
import random
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone
from apps.user.models import User
from apps.warehouse.models import Warehouse, WarehouseArea, WarehouseLocation
from apps.product.models import Category, Unit, Supplier, Product
from apps.inventory.models import Inventory
from apps.order.models import Customer, Order, OrderItem


class Command(BaseCommand):
    help = '初始化WMS系统基础数据'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('开始初始化WMS系统数据...'))
        
        with transaction.atomic():
            self.create_users()
            self.create_warehouses()
            self.create_product_categories()
            self.create_units()
            self.create_suppliers()
            self.create_customers()
            self.create_products()
            self.create_inventory()
            self.create_orders()
        
        self.stdout.write(self.style.SUCCESS('WMS系统数据初始化完成!'))

    def create_users(self):
        """创建初始用户"""
        self.stdout.write('创建用户...')
        
        # 创建超级管理员
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@example.com',
                password='admin123',
                first_name='超级',
                last_name='管理员',
                role='admin',
                phone='13800000000',
                department='系统管理部',
                position='系统管理员'
            )
        
        # 创建仓库经理
        if not User.objects.filter(username='manager').exists():
            User.objects.create_user(
                username='manager',
                email='manager@example.com',
                password='manager123',
                first_name='仓库',
                last_name='经理',
                role='manager',
                phone='13800000001',
                department='仓储部',
                position='仓库经理',
                is_staff=True
            )
        
        # 创建操作员
        if not User.objects.filter(username='operator').exists():
            User.objects.create_user(
                username='operator',
                email='operator@example.com',
                password='operator123',
                first_name='仓库',
                last_name='操作员',
                role='operator',
                phone='13800000002',
                department='仓储部',
                position='仓库操作员'
            )
        
        # 创建查看者
        if not User.objects.filter(username='viewer').exists():
            User.objects.create_user(
                username='viewer',
                email='viewer@example.com',
                password='viewer123',
                first_name='系统',
                last_name='查看者',
                role='viewer',
                phone='13800000003',
                department='财务部',
                position='财务专员'
            )
        
        self.stdout.write(self.style.SUCCESS('用户创建完成'))

    def create_warehouses(self):
        """创建仓库、库区和库位"""
        self.stdout.write('创建仓库、库区和库位...')
        
        # 创建主仓库
        main_warehouse, created = Warehouse.objects.get_or_create(
            code='WH001',
            defaults={
                'name': '主仓库',
                'address': '上海市浦东新区张江高科技园区',
                'contact_person': '张经理',
                'contact_phone': '13900000001',
                'manager': User.objects.get(username='manager'),
                'description': '公司主要仓库，存放大部分商品'
            }
        )
        
        # 创建次仓库
        second_warehouse, created = Warehouse.objects.get_or_create(
            code='WH002',
            defaults={
                'name': '次仓库',
                'address': '上海市嘉定区工业园区',
                'contact_person': '李经理',
                'contact_phone': '13900000002',
                'manager': User.objects.get(username='manager'),
                'description': '公司次要仓库，主要存放低频商品'
            }
        )
        
        # 为主仓库创建库区
        area_types = ['原料区', '成品区', '退货区', '待检区']
        for i, area_type in enumerate(area_types):
            area_code = f'A{i+1:02d}'
            area, created = WarehouseArea.objects.get_or_create(
                warehouse=main_warehouse,
                code=area_code,
                defaults={
                    'name': area_type,
                    'area_type': area_type,
                    'description': f'{main_warehouse.name}的{area_type}'
                }
            )
            
            # 为每个库区创建库位
            for j in range(1, 11):  # 每个库区10个库位
                location_code = f'{area_code}-L{j:02d}'
                WarehouseLocation.objects.get_or_create(
                    area=area,
                    code=location_code,
                    defaults={
                        'name': f'{area.name}库位{j}',
                        'location_type': '标准库位',
                        'max_capacity': 1000,
                        'current_capacity': 0,
                        'is_empty': True
                    }
                )
        
        # 为次仓库创建库区
        area_types = ['常温区', '冷藏区']
        for i, area_type in enumerate(area_types):
            area_code = f'B{i+1:02d}'
            area, created = WarehouseArea.objects.get_or_create(
                warehouse=second_warehouse,
                code=area_code,
                defaults={
                    'name': area_type,
                    'area_type': area_type,
                    'description': f'{second_warehouse.name}的{area_type}'
                }
            )
            
            # 为每个库区创建库位
            for j in range(1, 6):  # 每个库区5个库位
                location_code = f'{area_code}-L{j:02d}'
                WarehouseLocation.objects.get_or_create(
                    area=area,
                    code=location_code,
                    defaults={
                        'name': f'{area.name}库位{j}',
                        'location_type': '标准库位',
                        'max_capacity': 500,
                        'current_capacity': 0,
                        'is_empty': True
                    }
                )
        
        self.stdout.write(self.style.SUCCESS('仓库、库区和库位创建完成'))

    def create_product_categories(self):
        """创建商品分类"""
        self.stdout.write('创建商品分类...')
        
        # 创建一级分类
        categories = [
            {'code': 'C001', 'name': '电子产品', 'level': 1},
            {'code': 'C002', 'name': '服装', 'level': 1},
            {'code': 'C003', 'name': '食品', 'level': 1},
            {'code': 'C004', 'name': '日用品', 'level': 1},
        ]
        
        for cat in categories:
            category, created = Category.objects.get_or_create(
                code=cat['code'],
                defaults={
                    'name': cat['name'],
                    'level': cat['level'],
                    'description': f'{cat["name"]}分类'
                }
            )
        
        # 创建二级分类
        sub_categories = [
            {'code': 'C001-01', 'name': '手机', 'parent_code': 'C001', 'level': 2},
            {'code': 'C001-02', 'name': '电脑', 'parent_code': 'C001', 'level': 2},
            {'code': 'C001-03', 'name': '配件', 'parent_code': 'C001', 'level': 2},
            {'code': 'C002-01', 'name': '男装', 'parent_code': 'C002', 'level': 2},
            {'code': 'C002-02', 'name': '女装', 'parent_code': 'C002', 'level': 2},
            {'code': 'C003-01', 'name': '零食', 'parent_code': 'C003', 'level': 2},
            {'code': 'C003-02', 'name': '饮料', 'parent_code': 'C003', 'level': 2},
            {'code': 'C004-01', 'name': '清洁用品', 'parent_code': 'C004', 'level': 2},
            {'code': 'C004-02', 'name': '个人护理', 'parent_code': 'C004', 'level': 2},
        ]
        
        for sub_cat in sub_categories:
            parent = Category.objects.get(code=sub_cat['parent_code'])
            category, created = Category.objects.get_or_create(
                code=sub_cat['code'],
                defaults={
                    'name': sub_cat['name'],
                    'parent': parent,
                    'level': sub_cat['level'],
                    'description': f'{parent.name}-{sub_cat["name"]}分类'
                }
            )
        
        self.stdout.write(self.style.SUCCESS('商品分类创建完成'))

    def create_units(self):
        """创建计量单位"""
        self.stdout.write('创建计量单位...')
        
        units = [
            {'code': 'PCS', 'name': '个'},
            {'code': 'BOX', 'name': '盒'},
            {'code': 'PKG', 'name': '包'},
            {'code': 'KG', 'name': '千克'},
            {'code': 'L', 'name': '升'},
            {'code': 'M', 'name': '米'},
            {'code': 'SET', 'name': '套'},
        ]
        
        for unit in units:
            Unit.objects.get_or_create(
                code=unit['code'],
                defaults={
                    'name': unit['name'],
                    'description': f'{unit["name"]}计量单位'
                }
            )
        
        self.stdout.write(self.style.SUCCESS('计量单位创建完成'))

    def create_suppliers(self):
        """创建供应商"""
        self.stdout.write('创建供应商...')
        
        suppliers = [
            {
                'code': 'S001',
                'name': '上海电子科技有限公司',
                'contact_person': '王经理',
                'contact_phone': '13911111111',
                'address': '上海市浦东新区张江高科技园区',
                'email': 'contact@shanghaitech.com'
            },
            {
                'code': 'S002',
                'name': '广州服装制造有限公司',
                'contact_person': '李经理',
                'contact_phone': '13922222222',
                'address': '广州市天河区服装产业园',
                'email': 'contact@gzclothing.com'
            },
            {
                'code': 'S003',
                'name': '北京食品集团',
                'contact_person': '张经理',
                'contact_phone': '13933333333',
                'address': '北京市朝阳区食品工业园',
                'email': 'contact@bjfood.com'
            },
            {
                'code': 'S004',
                'name': '深圳日用品有限公司',
                'contact_person': '刘经理',
                'contact_phone': '13944444444',
                'address': '深圳市南山区科技园',
                'email': 'contact@szdaily.com'
            },
        ]
        
        for supplier in suppliers:
            Supplier.objects.get_or_create(
                code=supplier['code'],
                defaults={
                    'name': supplier['name'],
                    'contact_person': supplier['contact_person'],
                    'contact_phone': supplier['contact_phone'],
                    'address': supplier['address'],
                    'email': supplier['email'],
                    'description': f'{supplier["name"]}供应商'
                }
            )
        
        self.stdout.write(self.style.SUCCESS('供应商创建完成'))

    def create_customers(self):
        """创建客户"""
        self.stdout.write('创建客户...')
        
        customers = [
            {
                'code': 'C001',
                'name': '北京零售连锁有限公司',
                'contact_person': '赵经理',
                'contact_phone': '13955555555',
                'address': '北京市海淀区中关村',
                'email': 'contact@bjretail.com'
            },
            {
                'code': 'C002',
                'name': '上海商贸有限公司',
                'contact_person': '钱经理',
                'contact_phone': '13966666666',
                'address': '上海市黄浦区南京路',
                'email': 'contact@shcommerce.com'
            },
            {
                'code': 'C003',
                'name': '广州批发市场',
                'contact_person': '孙经理',
                'contact_phone': '13977777777',
                'address': '广州市白云区批发市场',
                'email': 'contact@gzmarket.com'
            },
            {
                'code': 'C004',
                'name': '深圳电子商务有限公司',
                'contact_person': '周经理',
                'contact_phone': '13988888888',
                'address': '深圳市福田区电子商务产业园',
                'email': 'contact@szecommerce.com'
            },
        ]
        
        for customer in customers:
            Customer.objects.get_or_create(
                code=customer['code'],
                defaults={
                    'name': customer['name'],
                    'contact_person': customer['contact_person'],
                    'contact_phone': customer['contact_phone'],
                    'address': customer['address'],
                    'email': customer['email'],
                    'description': f'{customer["name"]}客户'
                }
            )
        
        self.stdout.write(self.style.SUCCESS('客户创建完成'))

    def create_products(self):
        """创建商品"""
        self.stdout.write('创建商品...')
        
        products = [
            {
                'code': 'P001',
                'name': '智能手机',
                'barcode': '6901234567890',
                'category_code': 'C001-01',
                'unit_code': 'PCS',
                'supplier_code': 'S001',
                'spec': '6.1英寸',
                'price': 3999.00,
                'cost': 2999.00,
                'weight': 0.2,
                'volume': 0.001,
                'min_stock': 10,
                'max_stock': 100,
                'shelf_life': 730
            },
            {
                'code': 'P002',
                'name': '笔记本电脑',
                'barcode': '6901234567891',
                'category_code': 'C001-02',
                'unit_code': 'PCS',
                'supplier_code': 'S001',
                'spec': '15.6英寸',
                'price': 5999.00,
                'cost': 4999.00,
                'weight': 2.0,
                'volume': 0.01,
                'min_stock': 5,
                'max_stock': 50,
                'shelf_life': 1095
            },
            {
                'code': 'P003',
                'name': '男士T恤',
                'barcode': '6901234567892',
                'category_code': 'C002-01',
                'unit_code': 'PCS',
                'supplier_code': 'S002',
                'spec': 'XL',
                'price': 99.00,
                'cost': 49.00,
                'weight': 0.3,
                'volume': 0.002,
                'min_stock': 50,
                'max_stock': 500,
                'shelf_life': 1825
            },
            {
                'code': 'P004',
                'name': '女士连衣裙',
                'barcode': '6901234567893',
                'category_code': 'C002-02',
                'unit_code': 'PCS',
                'supplier_code': 'S002',
                'spec': 'M',
                'price': 199.00,
                'cost': 99.00,
                'weight': 0.5,
                'volume': 0.003,
                'min_stock': 30,
                'max_stock': 300,
                'shelf_life': 1825
            },
            {
                'code': 'P005',
                'name': '巧克力',
                'barcode': '6901234567894',
                'category_code': 'C003-01',
                'unit_code': 'BOX',
                'supplier_code': 'S003',
                'spec': '100g',
                'price': 29.90,
                'cost': 15.00,
                'weight': 0.1,
                'volume': 0.0005,
                'min_stock': 100,
                'max_stock': 1000,
                'shelf_life': 180
            },
            {
                'code': 'P006',
                'name': '矿泉水',
                'barcode': '6901234567895',
                'category_code': 'C003-02',
                'unit_code': 'BOX',
                'supplier_code': 'S003',
                'spec': '550ml*24瓶',
                'price': 39.90,
                'cost': 20.00,
                'weight': 13.2,
                'volume': 0.02,
                'min_stock': 50,
                'max_stock': 500,
                'shelf_life': 365
            },
            {
                'code': 'P007',
                'name': '洗衣液',
                'barcode': '6901234567896',
                'category_code': 'C004-01',
                'unit_code': 'BOX',
                'supplier_code': 'S004',
                'spec': '3kg',
                'price': 59.90,
                'cost': 30.00,
                'weight': 3.2,
                'volume': 0.005,
                'min_stock': 30,
                'max_stock': 300,
                'shelf_life': 730
            },
            {
                'code': 'P008',
                'name': '牙膏',
                'barcode': '6901234567897',
                'category_code': 'C004-02',
                'unit_code': 'BOX',
                'supplier_code': 'S004',
                'spec': '120g*3支',
                'price': 39.90,
                'cost': 20.00,
                'weight': 0.4,
                'volume': 0.001,
                'min_stock': 50,
                'max_stock': 500,
                'shelf_life': 730
            },
        ]
        
        for product in products:
            category = Category.objects.get(code=product['category_code'])
            unit = Unit.objects.get(code=product['unit_code'])
            supplier = Supplier.objects.get(code=product['supplier_code'])
            
            Product.objects.get_or_create(
                code=product['code'],
                defaults={
                    'name': product['name'],
                    'barcode': product['barcode'],
                    'category': category,
                    'unit': unit,
                    'supplier': supplier,
                    'spec': product['spec'],
                    'price': product['price'],
                    'cost': product['cost'],
                    'weight': product['weight'],
                    'volume': product['volume'],
                    'min_stock': product['min_stock'],
                    'max_stock': product['max_stock'],
                    'shelf_life': product['shelf_life'],
                    'description': f'{product["name"]} {product["spec"]}'
                }
            )
        
        self.stdout.write(self.style.SUCCESS('商品创建完成'))

    def create_inventory(self):
        """创建库存"""
        self.stdout.write('创建库存...')
        
        # 获取所有商品
        products = Product.objects.all()
        
        # 获取主仓库
        main_warehouse = Warehouse.objects.get(code='WH001')
        
        # 获取主仓库的成品区
        product_area = WarehouseArea.objects.get(warehouse=main_warehouse, name='成品区')
        
        # 获取成品区的库位
        locations = WarehouseLocation.objects.filter(area=product_area)
        
        # 为每个商品创建库存
        for i, product in enumerate(products):
            # 循环使用库位
            location = locations[i % len(locations)]
            
            # 生成批次号
            batch_number = f'BN{timezone.now().strftime("%Y%m%d")}{i+1:02d}'
            
            # 生成生产日期和过期日期
            production_date = timezone.now().date() - timedelta(days=random.randint(1, 30))
            expiry_date = production_date + timedelta(days=product.shelf_life) if product.shelf_life else None
            
            # 生成随机数量
            quantity = random.randint(int(product.min_stock), int(product.max_stock) if product.max_stock else 100)
            
            # 创建库存记录
            inventory, created = Inventory.objects.get_or_create(
                warehouse=main_warehouse,
                location=location,
                product=product,
                batch_number=batch_number,
                defaults={
                    'quantity': quantity,
                    'available_quantity': quantity,
                    'locked_quantity': 0,
                    'production_date': production_date,
                    'expiry_date': expiry_date,
                    'status': 'normal'
                }
            )
            
            # 更新库位状态
            if created:
                location.is_empty = False
                location.current_capacity += quantity
                location.save()
        
        self.stdout.write(self.style.SUCCESS('库存创建完成'))

    def create_orders(self):
        """创建订单"""
        self.stdout.write('创建订单...')
        
        # 获取仓库
        main_warehouse = Warehouse.objects.get(code='WH001')
        
        # 获取客户
        customers = Customer.objects.all()
        
        # 获取供应商
        suppliers = Supplier.objects.all()
        
        # 获取用户
        admin_user = User.objects.get(username='admin')
        manager_user = User.objects.get(username='manager')
        
        # 获取所有商品
        products = Product.objects.all()
        
        # 创建入库单
        inbound_order, created = Order.objects.get_or_create(
            order_code='IN' + timezone.now().strftime('%Y%m%d') + '001',
            defaults={
                'order_type': 'inbound',
                'status': 'completed',
                'warehouse': main_warehouse,
                'supplier': suppliers[0],
                'creator': admin_user,
                'handler': manager_user,
                'total_amount': 0,
                'order_date': timezone.now().date() - timedelta(days=7),
                'expected_date': timezone.now().date() - timedelta(days=5),
                'completion_date': timezone.now().date() - timedelta(days=5),
                'remark': '初始入库单'
            }
        )
        
        # 创建入库单明细
        if created:
            total_amount = 0
            for i, product in enumerate(products[:4]):  # 只使用前4个商品
                quantity = random.randint(10, 50)
                unit_price = product.cost
                total_price = quantity * unit_price
                total_amount += total_price
                
                OrderItem.objects.create(
                    order=inbound_order,
                    product=product,
                    quantity=quantity,
                    unit_price=unit_price,
                    total_price=total_price,
                    processed_quantity=quantity,
                    status='completed',
                    batch_number=f'BN{timezone.now().strftime("%Y%m%d")}{i+1:02d}',
                    production_date=timezone.now().date() - timedelta(days=random.randint(1, 30)),
                    expiry_date=timezone.now().date() + timedelta(days=product.shelf_life) if product.shelf_life else None
                )
            
            # 更新订单总金额
            inbound_order.total_amount = total_amount
            inbound_order.save()
        
        # 创建出库单
        outbound_order, created = Order.objects.get_or_create(
            order_code='OUT' + timezone.now().strftime('%Y%m%d') + '001',
            defaults={
                'order_type': 'outbound',
                'status': 'completed',
                'warehouse': main_warehouse,
                'customer': customers[0],
                'creator': admin_user,
                'handler': manager_user,
                'total_amount': 0,
                'order_date': timezone.now().date() - timedelta(days=3),
                'expected_date': timezone.now().date() - timedelta(days=2),
                'completion_date': timezone.now().date() - timedelta(days=2),
                'remark': '初始出库单'
            }
        )
        
        # 创建出库单明细
        if created:
            total_amount = 0
            for i, product in enumerate(products[4:]):  # 使用后4个商品
                quantity = random.randint(5, 20)
                unit_price = product.price
                total_price = quantity * unit_price
                total_amount += total_price
                
                OrderItem.objects.create(
                    order=outbound_order,
                    product=product,
                    quantity=quantity,
                    unit_price=unit_price,
                    total_price=total_price,
                    processed_quantity=quantity,
                    status='completed'
                )
            
            # 更新订单总金额
            outbound_order.total_amount = total_amount
            outbound_order.save()
        
        self.stdout.write(self.style.SUCCESS('订单创建完成'))
