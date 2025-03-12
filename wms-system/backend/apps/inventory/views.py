from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.http import FileResponse
from django.db.models import Sum, F
from django.utils.timezone import now
import pandas as pd
import io
from .models import Inventory, Transaction
from .serializers import InventorySerializer, TransactionSerializer
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