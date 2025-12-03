from django.contrib import admin
from .models import Circuit, Machine, SupplyLog

@admin.register(Circuit)
class CircuitAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'category', 'stock_qty', 'min_stock_limit', 'is_critical')
    list_filter = ('category',)
    search_fields = ('name', 'code')
    # is critical memamnggil boolean dari model.py

@admin.register(Machine)
class MachineAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'last_checked')
    list_editable = ('status',) # bisa ubah status langsung
    list_filter = ('status',)

@admin.register(SupplyLog)
class SupplyLogAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'transaction_type', 'circuit', 'quantity', 'pic_name')
    list_filter = ('transaction_type', 'timestamp')
    date_hierarchy = 'timestamp' 
