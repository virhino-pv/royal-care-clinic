from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Administrator'),
        ('doctor', 'Doctor / Specialist'),
        ('receptionist', 'Receptionist / Front Desk'),
        ('lab_technician', 'Lab Technician / Pathologist'),
        ('patient', 'Patient'),
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='receptionist')
    phone = models.CharField(max_length=20, unique=True, null=True, blank=True)
    address = models.TextField(blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    class Meta:
        ordering = ['username']
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        full = self.get_full_name()
        display = full if full else self.username
        return f"{display} ({self.get_role_display()})"

    @property
    def is_admin(self):
        return self.role == 'admin' or self.is_superuser

    @property
    def is_doctor(self):
        return self.role == 'doctor'

    @property
    def is_receptionist(self):
        return self.role == 'receptionist'

    @property
    def is_lab_technician(self):
        return self.role == 'lab_technician'

    @property
    def is_patient(self):
        return self.role == 'patient'

    @property
    def is_staff_member(self):
        return self.role in ['admin', 'doctor', 'receptionist', 'lab_technician'] or self.is_staff
