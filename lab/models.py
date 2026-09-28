from django.db import models
from django.utils import timezone
import uuid
from patients.models import Patient
from doctors.models import Doctor

class LabCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, default='bi-droplet-half', help_text='Bootstrap icon name')

    class Meta:
        verbose_name_plural = 'Lab Categories'
        ordering = ['name']

    def __str__(self):
        return self.name

class LabTest(models.Model):
    SAMPLE_CHOICES = (
        ('Blood', 'Whole Blood / Serum / Plasma'),
        ('Urine', 'Urine Sample'),
        ('Stool', 'Stool Sample'),
        ('Swab', 'Throat / Nasal Swab'),
        ('Sputum', 'Sputum Sample'),
        ('Fluid', 'Body Fluids / CSF / Synovial'),
        ('Other', 'Other Sample Type'),
    )

    category = models.ForeignKey(LabCategory, on_delete=models.CASCADE, related_name='tests')
    code = models.CharField(max_length=20, unique=True, help_text='e.g., CBC, LFT, KFT, HBA1C')
    name = models.CharField(max_length=200)
    sample_type = models.CharField(max_length=50, choices=SAMPLE_CHOICES, default='Blood')
    price = models.DecimalField(max_digits=8, decimal_places=2)
    turnaround_hours = models.PositiveIntegerField(default=4, help_text='Standard report delivery time in hours')
    normal_range = models.CharField(max_length=200, blank=True, help_text='Standard Reference Interval')
    unit = models.CharField(max_length=50, blank=True, help_text='Measurement unit (e.g. mg/dL, g/dL, %)')
    description = models.TextField(blank=True, help_text='Clinical significance and preparation instructions')
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['category', 'name']

    def __str__(self):
        return f"{self.name} ({self.code}) — ₹{self.price}"

class LabOrder(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending Sample Collection'),
        ('sample_collected', 'Sample Collected'),
        ('in_analysis', 'Under Testing / Analysis'),
        ('completed', 'Completed & Verified'),
        ('cancelled', 'Cancelled'),
    )

    PRIORITY_CHOICES = (
        ('routine', 'Routine'),
        ('urgent', 'Urgent'),
        ('stat', 'STAT (Emergency)'),
    )

    order_number = models.CharField(max_length=30, unique=True, blank=True, db_index=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='lab_orders')
    doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True, blank=True, related_name='lab_orders', help_text='Referring Doctor (optional)')
    order_date = models.DateField(default=timezone.now, db_index=True)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='pending', db_index=True)
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='routine')
    
    sample_collected_at = models.DateTimeField(null=True, blank=True)
    reported_at = models.DateTimeField(null=True, blank=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.order_number} — {self.patient.full_name} ({self.get_status_display()})"

    def calculate_total(self):
        total = sum(item.test.price for item in self.items.all())
        return total

    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = f"LAB-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)

class LabOrderItem(models.Model):
    order = models.ForeignKey(LabOrder, on_delete=models.CASCADE, related_name='items')
    test = models.ForeignKey(LabTest, on_delete=models.PROTECT)
    result_value = models.CharField(max_length=200, blank=True)
    reference_range = models.CharField(max_length=200, blank=True)
    unit = models.CharField(max_length=50, blank=True)
    is_abnormal = models.BooleanField(default=False)
    technician_remarks = models.TextField(blank=True)

    def __str__(self):
        return f"{self.test.name} for {self.order.order_number}"

    def save(self, *args, **kwargs):
        if not self.reference_range and self.test:
            self.reference_range = self.test.normal_range
        if not self.unit and self.test:
            self.unit = self.test.unit
        super().save(*args, **kwargs)
