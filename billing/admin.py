from django.contrib import admin
from .models import Invoice

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('invoice_number', 'patient', 'total_amount', 'paid_amount', 'payment_status', 'payment_method', 'created_at')
    list_filter = ('payment_status', 'payment_method', 'created_at')
    search_fields = ('invoice_number', 'patient__first_name', 'patient__last_name', 'patient__phone', 'transaction_reference')
