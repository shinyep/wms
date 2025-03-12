import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.warehouse.models import Warehouse

# 创建三个仓库
warehouses = [
    {
        'code': 'WH001',
        'name': '主仓库',
        'address': '上海市浦东新区张江高科技园区',
        'contact_person': '张三',
        'contact_phone': '13800138001',
        'description': '主要存储电子产品',
        'is_active': True
    },
    {
        'code': 'WH002',
        'name': '原材料仓库',
        'address': '上海市嘉定区工业园区',
        'contact_person': '李四',
        'contact_phone': '13800138002',
        'description': '存储生产原材料',
        'is_active': True
    },
    {
        'code': 'WH003',
        'name': '成品仓库',
        'address': '上海市松江区工业区',
        'contact_person': '王五',
        'contact_phone': '13800138003',
        'description': '存储成品',
        'is_active': True
    }
]

for warehouse_data in warehouses:
    Warehouse.objects.get_or_create(
        code=warehouse_data['code'],
        defaults=warehouse_data
    )

print('仓库创建完成！') 