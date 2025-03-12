from rest_framework import serializers
from apps.warehouse.serializers import WarehouseSerializer, WarehouseLocationSerializer
from apps.product.serializers import ProductSerializer
from apps.user.serializers import UserSerializer
from .models import Inventory, Transaction

class TransactionSerializer(serializers.ModelSerializer):
    warehouse = WarehouseSerializer(read_only=True)
    product = ProductSerializer(read_only=True)
    operator = UserSerializer(read_only=True)
    
    # 添加自定义字段展示
    display_transaction_type = serializers.SerializerMethodField()
    display_status = serializers.SerializerMethodField()
    display_date = serializers.SerializerMethodField()
    
    def get_display_transaction_type(self, obj):
        return '入库' if obj.transaction_type == 'IN' else '出库'
    
    def get_display_status(self, obj):
        status_map = {
            'pending': '待处理',
            'completed': '已完成',
            'cancelled': '已取消'
        }
        return status_map.get(obj.status, obj.status)
    
    def get_display_date(self, obj):
        return obj.transaction_date.strftime('%Y-%m-%d') if obj.transaction_date else ''
    
    class Meta:
        model = Transaction
        fields = [
            'id', 'transaction_code', 'display_date', 'product', 'spec',
            'unit', 'quantity', 'unit_price', 'amount', 'operator', 'warehouse',
            'display_transaction_type', 'display_status', 'remark',
            'created_time', 'updated_time', 'transaction_type', 'status',
            'transaction_date'
        ]
        read_only_fields = ['created_time', 'updated_time', 'amount']
        
    def to_representation(self, instance):
        data = super().to_representation(instance)
        # 转换为模板格式的数据结构
        return {
            '序号': data['id'],
            '日期': data['display_date'],
            '单据编号': data['transaction_code'],
            '品项': data['product']['name'] if data['product'] else '',
            '规格/型号': data['spec'] or (data['product']['spec'] if data['product'] else ''),
            '单位': data['unit'],
            '数量': data['quantity'],
            '单价': data['unit_price'],
            '金额': data['amount'],
            '经手人': data['operator']['name'] if data['operator'] else '',
            '类型': data['display_transaction_type'],
            '状态': data['display_status'],
            '备注': data['remark'] or ''
        }

class InventorySerializer(serializers.ModelSerializer):
    warehouse = WarehouseSerializer(read_only=True)
    location = WarehouseLocationSerializer(read_only=True)
    product = ProductSerializer(read_only=True)
    
    class Meta:
        model = Inventory
        fields = [
            'id', 'warehouse', 'location', 'product', 'spec', 'unit',
            'initial_quantity', 'total_in', 'total_out', 'quantity',
            'unit_price', 'amount', 'is_active', 'created_time', 'updated_time'
        ]
        read_only_fields = ['created_time', 'updated_time', 'amount']
        
    def to_representation(self, instance):
        data = super().to_representation(instance)
        # 转换为模板格式的数据结构
        return {
            '序号': data['id'],
            '位置': data['location']['code'] if data['location'] else '未分配',
            '品项': data['product']['name'] if data['product'] else '',
            '规格/型号': data['spec'] or (data['product']['spec'] if data['product'] else ''),
            '单位': data['unit'],
            '期初库存': data['initial_quantity'],
            '累计入库': data['total_in'],
            '累计出库': data['total_out'],
            '库存': data['quantity'],
            '单价': data['unit_price'],
            '库存金额': data['amount'],
            '状态': '启用' if data['is_active'] else '禁用'
        } 