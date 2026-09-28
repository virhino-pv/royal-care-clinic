from django.contrib import admin
from .models import Appointment

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'appointment_date', 'appointment_time', 'status', 'appointment_type', 'fee')
    list_filter = ('status', 'appointment_type', 'appointment_date', 'doctor')
    search_fields = ('patient__first_name', 'patient__last_name', 'patient__phone', 'doctor__user__first_name', 'doctor__user__last_name')
