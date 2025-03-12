from rest_framework import serializers
from .models import Warehouse, WarehouseArea, WarehouseLocation, Report

class WarehouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warehouse
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']

class WarehouseAreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = WarehouseArea
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']

class WarehouseLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = WarehouseLocation
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']

class ReportSerializer(serializers.ModelSerializer):
    creator_name = serializers.SerializerMethodField()
    warehouse_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Report
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at', 'creator', 'creator_name', 'warehouse_name']
        
    def get_creator_name(self, obj):
        if obj.creator:
            return obj.creator.username
        return None
        
    def get_warehouse_name(self, obj):
        return obj.warehouse.name 