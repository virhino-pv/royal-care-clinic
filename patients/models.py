from django.db import models
from datetime import date
import re

class Patient(models.Model):
    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    )

    BLOOD_GROUP_CHOICES = (
        ('A+', 'A+'), ('A-', 'A-'),
        ('B+', 'B+'), ('B-', 'B-'),
        ('O+', 'O+'), ('O-', 'O-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'),
        ('Unknown', 'Unknown'),
    )

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=20, unique=True, db_index=True)
    email = models.EmailField(blank=True, null=True)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='other')
    blood_group = models.CharField(max_length=10, choices=BLOOD_GROUP_CHOICES, default='Unknown')
    
    address = models.TextField(blank=True)
    emergency_contact = models.CharField(max_length=100, blank=True, help_text='Name & Phone')
    allergies = models.TextField(blank=True, help_text='Known drug/food allergies')
    medical_history = models.TextField(blank=True, help_text='Past illnesses, chronic conditions, surgeries')
    
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['phone']),
            models.Index(fields=['first_name', 'last_name']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        full = f"{self.first_name} {self.last_name}".strip()
        return f"{full} ({self.phone})"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip()

    @property
    def age(self):
        if not self.date_of_birth:
            return 'N/A'
        today = date.today()
        return today.year - self.date_of_birth.year - (
            (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
        )

    @property
    def is_returning(self):
        # A patient is returning if they have attended more than 1 appointment or order
        return self.appointments.count() > 1 or self.lab_orders.count() > 1

    @staticmethod
    def validate_phone(phone_str):
        clean = re.sub(r'[\s\-\(\)\+]', '', phone_str)
        return len(clean) >= 10 and clean.isdigit()
