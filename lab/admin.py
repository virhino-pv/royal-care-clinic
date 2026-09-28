from django.contrib import admin
from .models import LabCategory, LabTest, LabOrder, LabOrderItem

class LabOrderItemInline(admin.TabularInline):
    model = LabOrderItem
    extra = 1

@admin.register(LabCategory)
class LabCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'icon')

@admin.register(LabTest)
class LabTestAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'category', 'sample_type', 'price', 'turnaround_hours', 'is_active')
    list_filter = ('category', 'sample_type', 'is_active')
    search_fields = ('name', 'code')

@admin.register(LabOrder)
class LabOrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'patient', 'doctor', 'order_date', 'status', 'priority', 'total_amount')
    list_filter = ('status', 'priority', 'order_date')
    search_fields = ('order_number', 'patient__first_name', 'patient__last_name', 'patient__phone')
    inlines = [LabOrderItemInline]
