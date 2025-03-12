from django.contrib import admin
from .models import Warehouse, WarehouseArea, WarehouseLocation

@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'contact_person', 'contact_phone', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('code', 'name', 'contact_person')

@admin.register(WarehouseArea)
class WarehouseAreaAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'warehouse', 'area_type', 'is_active')
    list_filter = ('warehouse', 'is_active')
    search_fields = ('code', 'name')

@admin.register(WarehouseLocation)
class WarehouseLocationAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'area', 'location_type', 'is_active', 'is_empty')
    list_filter = ('area', 'is_active', 'is_empty')
    search_fields = ('code', 'name') 