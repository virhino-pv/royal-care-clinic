from django.contrib import admin
from .models import Patient

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'phone', 'email', 'gender', 'blood_group', 'age', 'created_at')
    search_fields = ('first_name', 'last_name', 'phone', 'email')
    list_filter = ('gender', 'blood_group', 'created_at')
    readonly_fields = ('created_at', 'updated_at')
