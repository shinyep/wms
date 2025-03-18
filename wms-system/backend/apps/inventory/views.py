from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.http import FileResponse
from django.db.models import Sum, F
from django.utils.timezone import now
import pandas as pd
import io
import uuid
from datetime import datetime
from django.db import transaction as db_transaction
from .models import Inventory, Transaction, StockCheck, StockCheckItem
from .serializers import (
    InventorySerializer, 
    TransactionSerializer, 
    StockCheckSerializer, 
    StockCheckItemSerializer
)
from ..user.views import InventoryViewPermission

class InventoryViewSet(viewsets.ModelViewSet):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer
    permission_classes = [InventoryViewPermission]
    filterset_fields = ['warehouse', 'location', 'product', 'is_active']
    search_fields = ['product__name', 'product__code', 'location__code']
    ordering_fields = ['id', 'created_time', 'quantity', 'amount']
    ordering = ['-created_time']

    @action(detail=False, methods=['get'])
    def export_inventory(self, request):
        """导出库存详情"""
        try:
            warehouse_id = request.query_params.get('warehouse_id')
            
            # 准备查询条件
            query_params = {'is_active': True}
            if warehouse_id:
                query_params['warehouse_id'] = warehouse_id
            
            # 获取库存记录
            inventory_records = self.get_queryset().filter(
                **query_params
            ).select_related(
                'warehouse',
                'product',
                'location'
            ).order_by('location__code', 'product__code')
            
            # 准备数据列表
            data_list = []
            for index, record in enumerate(inventory_records, 1):
                data_list.append({
                    '序号': index,
                    '位置': record.location.code if record.location else '未分配',
                    '品项': record.product.name,
                    '规格/型号': record.spec or record.product.spec or '',
                    '单位': record.unit or record.product.unit.name if record.product.unit else '',
                    '期初库存': record.initial_quantity,
                    '累计入库': record.total_in,
                    '累计出库': record.total_out,
                    '库存': record.quantity,
                    '单价': record.unit_price,
                    '库存金额': record.amount
                })
            
            # 创建DataFrame
            df = pd.DataFrame(data_list)
            
            # 创建一个BytesIO对象
            excel_file = io.BytesIO()
            
            # 将DataFrame写入Excel
            writer = pd.ExcelWriter(excel_file, engine='openpyxl')
            df.to_excel(writer, sheet_name='库存详细列表', index=False)
            
            # 设置列宽
            worksheet = writer.sheets['库存详细列表']
            for idx, col in enumerate(df.columns):
                max_length = max(df[col].astype(str).apply(len).max(), len(col))
                worksheet.column_dimensions[chr(65 + idx)].width = max_length + 2
            
            # 保存并关闭
            writer.close()
            excel_file.seek(0)
            
            # 生成文件名
            filename = f'库存详细列表_{now().strftime("%Y%m%d_%H%M%S")}.xlsx'
            
            # 创建FileResponse
            response = FileResponse(
                excel_file,
                as_attachment=True,
                filename=filename,
                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
            
            return response
            
        except Exception as e:
            return Response(
                {'error': f'导出失败: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [InventoryViewPermission]
    filterset_fields = ['warehouse', 'product', 'transaction_type', 'status']
    search_fields = ['transaction_code', 'product__name', 'product__code']
    ordering_fields = ['transaction_date', 'created_time', 'amount']
    ordering = ['-transaction_date', '-created_time']

    @action(detail=False, methods=['get'])
    def export_transactions(self, request):
        """导出出入库记录"""
        try:
            warehouse_id = request.query_params.get('warehouse_id')
            transaction_type = request.query_params.get('type')
            start_date = request.query_params.get('start_date')
            end_date = request.query_params.get('end_date')
            
            # 准备查询条件
            query_params = {'status': 'completed'}
            if warehouse_id:
                query_params['warehouse_id'] = warehouse_id
            if transaction_type:
                query_params['transaction_type'] = transaction_type
            if start_date:
                query_params['transaction_date__gte'] = start_date
            if end_date:
                query_params['transaction_date__lte'] = end_date
            
            # 获取交易记录
            transactions = self.get_queryset().filter(
                **query_params
            ).select_related(
                'warehouse',
                'product',
                'operator'
            ).order_by('-transaction_date', 'transaction_code')
            
            # 准备数据列表
            data_list = []
            for index, record in enumerate(transactions, 1):
                data_list.append({
                    '序号': index,
                    '日期': record.transaction_date,
                    '品项': record.product.name,
                    '规格/型号': record.spec or record.product.spec or '',
                    '单位': record.unit or record.product.unit.name if record.product.unit else '',
                    '数量': record.quantity,
                    '单价': record.unit_price,
                    '金额': record.amount,
                    '经手人': record.operator.name if record.operator else ''
                })
            
            # 创建DataFrame
            df = pd.DataFrame(data_list)
            
            # 创建一个BytesIO对象
            excel_file = io.BytesIO()
            
            # 将DataFrame写入Excel
            writer = pd.ExcelWriter(excel_file, engine='openpyxl')
            sheet_name = '月入库详情' if transaction_type == 'IN' else '月出库详情'
            df.to_excel(writer, sheet_name=sheet_name, index=False)
            
            # 设置列宽
            worksheet = writer.sheets[sheet_name]
            for idx, col in enumerate(df.columns):
                max_length = max(df[col].astype(str).apply(len).max(), len(col))
                worksheet.column_dimensions[chr(65 + idx)].width = max_length + 2
            
            # 保存并关闭
            writer.close()
            excel_file.seek(0)
            
            # 生成文件名
            type_text = '入库' if transaction_type == 'IN' else '出库' if transaction_type == 'OUT' else '出入库'
            filename = f'月{type_text}详情_{now().strftime("%Y%m%d_%H%M%S")}.xlsx'
            
            # 创建FileResponse
            response = FileResponse(
                excel_file,
                as_attachment=True,
                filename=filename,
                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
            
            return response
            
        except Exception as e:
            return Response(
                {'error': f'导出失败: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class StockCheckViewSet(viewsets.ModelViewSet):
    """库存盘点视图集"""
    queryset = StockCheck.objects.all()
    serializer_class = StockCheckSerializer
    permission_classes = [InventoryViewPermission]
    filterset_fields = ['warehouse', 'status', 'check_type']
    search_fields = ['check_code', 'warehouse__name', 'creator__username', 'checker__username']
    ordering_fields = ['created_time', 'start_time', 'end_time']
    ordering = ['-created_time']
    
    def perform_create(self, serializer):
        """创建盘点单时自动生成盘点单号"""
        check_code = f"SC{datetime.now().strftime('%Y%m%d%H%M%S')}{str(uuid.uuid4())[:4]}"
        serializer.save(
            check_code=check_code,
            creator=self.request.user
        )
    
    @action(detail=True, methods=['post'])
    def start_check(self, request, pk=None):
        """开始盘点"""
        try:
            stock_check = self.get_object()
            
            # 检查当前状态是否允许开始盘点
            if stock_check.status != 'draft':
                return Response(
                    {'error': f'当前状态({stock_check.get_status_display()})不允许开始盘点'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # 使用事务确保数据一致性
            with db_transaction.atomic():
                # 更新盘点单状态和开始时间
                stock_check.status = 'in_progress'
                stock_check.start_time = now()
                stock_check.save()
                
                # 如果盘点明细为空，则自动创建盘点明细
                if not stock_check.items.exists():
                    self._create_check_items(stock_check)
                
                return Response(
                    {'message': '盘点已开始', 'items_count': stock_check.items.count()},
                    status=status.HTTP_200_OK
                )
        except Exception as e:
            return Response(
                {'error': f'开始盘点失败: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=True, methods=['post'])
    def complete_check(self, request, pk=None):
        """完成盘点"""
        try:
            stock_check = self.get_object()
            
            # 检查当前状态是否允许完成盘点
            if stock_check.status != 'in_progress':
                return Response(
                    {'error': f'当前状态({stock_check.get_status_display()})不允许完成盘点'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # 检查是否有未盘点的明细
            pending_items = stock_check.items.filter(status='pending')
            if pending_items.exists():
                return Response(
                    {'error': f'还有{pending_items.count()}个商品未盘点，无法完成盘点'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # 使用事务确保数据一致性
            with db_transaction.atomic():
                # 更新盘点单状态和结束时间
                stock_check.status = 'completed'
                stock_check.end_time = now()
                stock_check.checker = request.user
                stock_check.save()
                
                # 调整库存（可选，根据业务需求）
                if request.data.get('adjust_inventory', False):
                    self._adjust_inventory(stock_check)
                
                return Response(
                    {'message': '盘点已完成'},
                    status=status.HTTP_200_OK
                )
        except Exception as e:
            return Response(
                {'error': f'完成盘点失败: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=True, methods=['post'])
    def cancel_check(self, request, pk=None):
        """取消盘点"""
        try:
            stock_check = self.get_object()
            
            # 检查当前状态是否允许取消盘点
            if stock_check.status in ['completed', 'cancelled']:
                return Response(
                    {'error': f'当前状态({stock_check.get_status_display()})不允许取消盘点'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # 更新盘点单状态
            stock_check.status = 'cancelled'
            stock_check.save()
            
            return Response(
                {'message': '盘点已取消'},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {'error': f'取消盘点失败: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=True, methods=['get'])
    def export_check(self, request, pk=None):
        """导出盘点单"""
        try:
            stock_check = self.get_object()
            
            # 获取盘点明细
            check_items = stock_check.items.select_related(
                'product',
                'location'
            ).order_by('product__name')
            
            # 准备数据列表
            data_list = []
            for index, item in enumerate(check_items, 1):
                status_display = '待盘点'
                if item.status == 'checked':
                    status_display = '已盘点'
                elif item.status == 'adjusted':
                    status_display = '已调整'
                
                data_list.append({
                    '序号': index,
                    '位置': item.location.code if item.location else '未分配',
                    '品项': item.product.name,
                    '规格/型号': item.product.spec or '',
                    '单位': item.product.unit.name if hasattr(item.product, 'unit') and item.product.unit else '',
                    '系统数量': item.system_quantity,
                    '实际数量': item.actual_quantity,
                    '差异数量': item.difference,
                    '状态': status_display,
                    '盘点时间': item.check_time.strftime('%Y-%m-%d %H:%M:%S') if item.check_time else '',
                    '备注': item.remark or ''
                })
            
            # 创建DataFrame
            df = pd.DataFrame(data_list)
            
            # 创建一个BytesIO对象
            excel_file = io.BytesIO()
            
            # 将DataFrame写入Excel
            writer = pd.ExcelWriter(excel_file, engine='openpyxl')
            df.to_excel(writer, sheet_name='盘点明细', index=False)
            
            # 设置列宽
            worksheet = writer.sheets['盘点明细']
            for idx, col in enumerate(df.columns):
                max_length = max(df[col].astype(str).apply(len).max(), len(col))
                worksheet.column_dimensions[chr(65 + idx)].width = max_length + 2
            
            # 保存并关闭
            writer.close()
            excel_file.seek(0)
            
            # 生成文件名
            filename = f'盘点单_{stock_check.check_code}_{now().strftime("%Y%m%d_%H%M%S")}.xlsx'
            
            # 创建FileResponse
            response = FileResponse(
                excel_file,
                as_attachment=True,
                filename=filename,
                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
            
            return response
            
        except Exception as e:
            return Response(
                {'error': f'导出失败: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def _create_check_items(self, stock_check):
        """创建盘点明细项"""
        # 获取仓库的库存记录
        warehouse = stock_check.warehouse
        query_params = {'warehouse': warehouse, 'is_active': True}
        
        # 对于部分盘点，可以添加更多过滤条件（示例）
        if stock_check.check_type == 'partial' and hasattr(stock_check, 'check_filter'):
            check_filter = stock_check.check_filter
            if check_filter.get('locations'):
                query_params['location__id__in'] = check_filter.get('locations')
            if check_filter.get('products'):
                query_params['product__id__in'] = check_filter.get('products')
        
        # 获取符合条件的库存记录
        inventory_items = Inventory.objects.filter(**query_params).select_related(
            'product',
            'location'
        )
        
        # 创建盘点明细
        check_items = []
        for inventory in inventory_items:
            check_item = StockCheckItem(
                stock_check=stock_check,
                product=inventory.product,
                location=inventory.location,
                system_quantity=inventory.quantity,
                actual_quantity=0,  # 初始为0，等待实际盘点
                difference=-inventory.quantity,  # 初始差异为负的系统库存
                status='pending'
            )
            check_items.append(check_item)
        
        # 批量创建
        if check_items:
            StockCheckItem.objects.bulk_create(check_items)
    
    def _adjust_inventory(self, stock_check):
        """根据盘点结果调整库存"""
        # 获取所有有差异的盘点明细
        diff_items = stock_check.items.exclude(difference=0)
        
        for item in diff_items:
            try:
                # 查找对应的库存记录
                inventory = Inventory.objects.get(
                    warehouse=stock_check.warehouse,
                    product=item.product,
                    location=item.location
                )
                
                # 调整库存数量
                inventory.quantity = item.actual_quantity
                inventory.save()
                
                # 更新盘点明细状态
                item.status = 'adjusted'
                item.save()
                
                # 创建库存调整记录（可选）
                if item.difference > 0:
                    # 实际数量大于系统数量，创建入库记录
                    self._create_adjustment_transaction(
                        stock_check, item, 'IN', item.difference
                    )
                elif item.difference < 0:
                    # 实际数量小于系统数量，创建出库记录
                    self._create_adjustment_transaction(
                        stock_check, item, 'OUT', abs(item.difference)
                    )
            except Inventory.DoesNotExist:
                # 如果找不到库存记录，但实际盘点数量大于0，则创建新的库存记录
                if item.actual_quantity > 0:
                    Inventory.objects.create(
                        warehouse=stock_check.warehouse,
                        product=item.product,
                        location=item.location,
                        quantity=item.actual_quantity,
                        unit_price=0,  # 初始单价设为0，需要后续更新
                        is_active=True
                    )
                    
                    # 更新盘点明细状态
                    item.status = 'adjusted'
                    item.save()
                    
                    # 创建库存调整入库记录
                    self._create_adjustment_transaction(
                        stock_check, item, 'IN', item.actual_quantity
                    )
    
    def _create_adjustment_transaction(self, stock_check, check_item, transaction_type, quantity):
        """创建库存调整的出入库记录"""
        transaction_code = f"ADJ{datetime.now().strftime('%Y%m%d%H%M%S')}{str(uuid.uuid4())[:4]}"
        
        # 创建出入库记录
        Transaction.objects.create(
            transaction_code=transaction_code,
            transaction_date=now().date(),
            product=check_item.product,
            spec=check_item.product.spec,
            unit=check_item.product.unit.name if hasattr(check_item.product, 'unit') and check_item.product.unit else '个',
            quantity=quantity,
            unit_price=0,  # 调整记录的单价设为0
            amount=0,  # 金额也设为0
            operator=stock_check.checker,
            warehouse=stock_check.warehouse,
            transaction_type=transaction_type,
            status='completed',
            remark=f'盘点调整: {stock_check.check_code}'
        )

class StockCheckItemViewSet(viewsets.ModelViewSet):
    """库存盘点明细视图集"""
    queryset = StockCheckItem.objects.all()
    serializer_class = StockCheckItemSerializer
    permission_classes = [InventoryViewPermission]
    filterset_fields = ['stock_check', 'product', 'location', 'status']
    search_fields = ['product__name', 'product__code', 'location__code']
    ordering_fields = ['id', 'check_time']
    ordering = ['id']
    
    @action(detail=True, methods=['post'])
    def update_actual_quantity(self, request, pk=None):
        """更新实际盘点数量"""
        try:
            check_item = self.get_object()
            
            # 检查盘点单状态
            stock_check = check_item.stock_check
            if stock_check.status != 'in_progress':
                return Response(
                    {'error': f'盘点单当前状态({stock_check.get_status_display()})不允许更新盘点数量'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # 获取实际数量
            actual_quantity = request.data.get('actual_quantity')
            if actual_quantity is None:
                return Response(
                    {'error': '缺少实际数量参数'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            try:
                actual_quantity = float(actual_quantity)
                if actual_quantity < 0:
                    return Response(
                        {'error': '实际数量不能为负数'}, 
                        status=status.HTTP_400_BAD_REQUEST
                    )
            except ValueError:
                return Response(
                    {'error': '实际数量必须是数字'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # 更新实际数量和差异数量
            check_item.actual_quantity = actual_quantity
            check_item.difference = actual_quantity - check_item.system_quantity
            check_item.status = 'checked'
            check_item.check_time = now()
            check_item.save()
            
            return Response(
                {
                    'message': '更新成功',
                    'actual_quantity': check_item.actual_quantity,
                    'system_quantity': check_item.system_quantity,
                    'difference': check_item.difference
                },
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {'error': f'更新盘点数量失败: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )