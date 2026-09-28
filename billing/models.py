from django.db import models
import uuid
from patients.models import Patient
from appointments.models import Appointment
from lab.models import LabOrder

class Invoice(models.Model):
    PAYMENT_STATUS = (
        ('unpaid', 'Unpaid'),
        ('partial', 'Partially Paid'),
        ('paid', 'Fully Paid'),
        ('refunded', 'Refunded'),
    )

    PAYMENT_METHOD = (
        ('cash', 'Cash Payment'),
        ('upi', 'UPI / QR Code / GPay / PhonePe'),
        ('card', 'Credit / Debit Card (POS)'),
        ('net_banking', 'Net Banking / IMPS / NEFT'),
    )

    invoice_number = models.CharField(max_length=30, unique=True, blank=True, db_index=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='invoices')
    appointment = models.OneToOneField(Appointment, on_delete=models.SET_NULL, null=True, blank=True, related_name='invoice')
    lab_order = models.OneToOneField(LabOrder, on_delete=models.SET_NULL, null=True, blank=True, related_name='invoice')

    # Line Item Breakdown
    consultation_charges = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    lab_charges = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    medicine_charges = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    other_charges = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='unpaid', db_index=True)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD, default='cash')
    transaction_reference = models.CharField(max_length=100, blank=True, help_text='UPI Ref ID / Card Txn ID')
    notes = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['created_at', 'payment_status']),
            models.Index(fields=['payment_method']),
        ]

    def __str__(self):
        return f"{self.invoice_number} — {self.patient.full_name} (₹{self.total_amount})"

    @property
    def balance_due(self):
        return max(0, self.total_amount - self.paid_amount)

    def calculate_totals(self):
        from decimal import Decimal
        def to_dec(val):
            if val is None:
                return Decimal('0.00')
            return Decimal(str(val))

        subtotal = (
            to_dec(self.consultation_charges) +
            to_dec(self.lab_charges) +
            to_dec(self.medicine_charges) +
            to_dec(self.other_charges)
        )
        total = (subtotal - to_dec(self.discount_amount)) + to_dec(self.tax_amount)
        return max(Decimal('0.00'), total)

    def save(self, *args, **kwargs):
        if not self.invoice_number:
            self.invoice_number = f"RC-{uuid.uuid4().hex[:8].upper()}"
        
        self.total_amount = self.calculate_totals()
        
        # Auto update payment status based on paid amount
        if self.paid_amount >= self.total_amount and self.total_amount > 0:
            self.payment_status = 'paid'
        elif self.paid_amount > 0 and self.paid_amount < self.total_amount:
            self.payment_status = 'partial'
        elif self.paid_amount == 0 and self.payment_status not in ['refunded']:
            self.payment_status = 'unpaid'

        super().save(*args, **kwargs)
