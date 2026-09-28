from django.contrib import admin
from .models import Prescription, PrescriptionMedicine

class PrescriptionMedicineInline(admin.TabularInline):
    model = PrescriptionMedicine
    extra = 1

@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ('appointment', 'diagnosis', 'follow_up_date', 'created_at')
    search_fields = ('appointment__patient__first_name', 'appointment__patient__last_name', 'diagnosis')
    inlines = [PrescriptionMedicineInline]
