from django.db import models
from appointments.models import Appointment

class Prescription(models.Model):
    appointment = models.OneToOneField(
        Appointment,
        on_delete=models.CASCADE,
        related_name='prescription'
    )
    diagnosis = models.TextField(help_text='Primary and differential diagnosis')
    chief_complaints = models.TextField(blank=True, help_text='Patient reported symptoms')
    
    # Clinical Vitals
    blood_pressure = models.CharField(max_length=20, blank=True, placeholder='e.g. 120/80 mmHg') if hasattr(models.CharField, 'placeholder') else models.CharField(max_length=20, blank=True, help_text='e.g. 120/80 mmHg')
    pulse_rate = models.CharField(max_length=20, blank=True, help_text='e.g. 72 bpm')
    temperature = models.CharField(max_length=20, blank=True, help_text='e.g. 98.4 F')
    weight_kg = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True, help_text='Patient weight in kg')
    
    advice_diet = models.TextField(blank=True, help_text='Lifestyle, diet and recovery advice')
    follow_up_date = models.DateField(null=True, blank=True, help_text='Recommended follow-up visit date')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Prescription for {self.appointment.patient.full_name} (Dr. {self.appointment.doctor.doctor_name})"

class PrescriptionMedicine(models.Model):
    FREQUENCY_CHOICES = (
        ('1-0-1 (Twice Daily After Food)', '1-0-1 (Twice Daily After Food)'),
        ('1-0-0 (Once Morning After Food)', '1-0-0 (Once Morning After Food)'),
        ('0-0-1 (Once Night After Food)', '0-0-1 (Once Night After Food)'),
        ('1-1-1 (Thrice Daily After Food)', '1-1-1 (Thrice Daily After Food)'),
        ('1-0-0 (Empty Stomach)', '1-0-0 (Empty Stomach / Before Food)'),
        ('SOS (As Needed)', 'SOS (As Needed / When Required)'),
        ('Custom', 'Custom Dosage Schedule'),
    )

    prescription = models.ForeignKey(Prescription, on_delete=models.CASCADE, related_name='medicines')
    medicine_name = models.CharField(max_length=200, help_text='Brand or Generic Name (e.g. Paracetamol 650mg, Pantocid 40mg)')
    dosage = models.CharField(max_length=50, help_text='e.g. 1 Tablet, 5ml, 1 Capsule')
    frequency = models.CharField(max_length=100, choices=FREQUENCY_CHOICES, default='1-0-1 (Twice Daily After Food)')
    duration_days = models.PositiveIntegerField(default=5, help_text='Days to continue')
    instructions = models.CharField(max_length=200, blank=True, help_text='Special instructions (e.g. take with warm water)')

    def __str__(self):
        return f"{self.medicine_name} - {self.dosage} ({self.duration_days} days)"
