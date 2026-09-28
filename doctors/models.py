from django.db import models
from django.conf import settings
from datetime import datetime, timedelta, time

class Doctor(models.Model):
    SPECIALTY_CHOICES = (
        ('General Physician', 'General Physician & Internal Medicine'),
        ('Cardiologist', 'Cardiology & Heart Care'),
        ('Diabetologist', 'Diabetology & Endocrinology'),
        ('Pediatrician', 'Pediatrics & Child Health'),
        ('Gynecologist', 'Obstetrics & Gynecology'),
        ('Dermatologist', 'Dermatology & Skin Care'),
        ('Orthopedist', 'Orthopedics & Joint Care'),
        ('ENT Specialist', 'Ear, Nose & Throat (ENT)'),
        ('Pathologist', 'Pathology & Lab Diagnostics'),
    )

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='doctor_profile'
    )
    specialization = models.CharField(max_length=100, choices=SPECIALTY_CHOICES, default='General Physician')
    qualification = models.CharField(max_length=200, help_text='e.g., MBBS, MD (General Medicine), DNB')
    experience_years = models.PositiveIntegerField(default=1)
    consultation_fee = models.DecimalField(max_digits=8, decimal_places=2, default=400.00)
    room_number = models.CharField(max_length=20, default='OPD-1', help_text='Consulting Room No.')
    photo = models.ImageField(upload_to='doctors/', blank=True, null=True)
    bio = models.TextField(blank=True, help_text='Professional background and clinical focus')
    
    # Schedule settings
    available_days = models.CharField(
        max_length=100,
        default='Monday,Tuesday,Wednesday,Thursday,Friday,Saturday',
        help_text='Comma-separated days'
    )
    start_time = models.TimeField(default='09:00:00', help_text='Consulting Start Time')
    end_time = models.TimeField(default='18:00:00', help_text='Consulting End Time')
    slot_duration_minutes = models.PositiveIntegerField(default=15, help_text='Minutes per patient slot')
    is_available = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['specialization', 'user__first_name']

    def __str__(self):
        return f"Dr. {self.user.get_full_name()} — {self.specialization}"

    @property
    def doctor_name(self):
        return f"Dr. {self.user.get_full_name()}" if self.user.get_full_name() else f"Dr. {self.user.username}"

    def get_available_days_list(self):
        return [d.strip() for d in self.available_days.split(',') if d.strip()]

    def generate_time_slots(self, target_date=None):
        """Returns list of time slot objects / strings between start_time and end_time"""
        slots = []
        current = datetime.combine(datetime.today(), self.start_time)
        end = datetime.combine(datetime.today(), self.end_time)

        while current < end:
            slots.append(current.time().strftime('%H:%M'))
            current += timedelta(minutes=self.slot_duration_minutes)
        return slots
