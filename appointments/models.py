from django.db import models
from django.utils import timezone
from datetime import datetime, date
from patients.models import Patient
from doctors.models import Doctor

class Appointment(models.Model):
    STATUS_CHOICES = (
        ('scheduled', 'Scheduled'),
        ('confirmed', 'Confirmed'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('no_show', 'No-Show / Absent'),
    )

    TYPE_CHOICES = (
        ('consultation', 'Initial Consultation'),
        ('follow_up', 'Follow-up Visit'),
        ('emergency', 'Emergency Walk-in'),
        ('report_review', 'Lab Report Review'),
    )

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name='appointments'
    )
    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.CASCADE,
        related_name='appointments'
    )
    appointment_date = models.DateField(db_index=True)
    appointment_time = models.TimeField()
    appointment_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='consultation')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled', db_index=True)
    
    fee = models.DecimalField(max_digits=8, decimal_places=2, default=400.00)
    reason = models.TextField(blank=True, help_text='Symptoms or purpose of visit')
    doctor_notes = models.TextField(blank=True, help_text='Internal clinical notes')
    reminder_sent = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-appointment_date', '-appointment_time']
        unique_together = ['doctor', 'appointment_date', 'appointment_time']
        indexes = [
            models.Index(fields=['appointment_date', 'status']),
            models.Index(fields=['doctor', 'appointment_date']),
        ]

    def __str__(self):
        return f"{self.patient.full_name} with {self.doctor.doctor_name} on {self.appointment_date} at {self.appointment_time.strftime('%I:%M %p')}"

    @property
    def is_past(self):
        appt_dt = datetime.combine(self.appointment_date, self.appointment_time)
        return appt_dt < datetime.now()

    @property
    def hour_slot(self):
        return self.appointment_time.hour
