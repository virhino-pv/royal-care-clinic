from django import forms
from .models import Invoice

class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = [
            'patient', 'appointment', 'lab_order',
            'consultation_charges', 'lab_charges', 'medicine_charges', 'other_charges',
            'discount_amount', 'tax_amount', 'paid_amount',
            'payment_status', 'payment_method', 'transaction_reference', 'notes'
        ]
        widgets = {
            'patient': forms.Select(attrs={'class': 'form-select select2-enable'}),
            'appointment': forms.Select(attrs={'class': 'form-select'}),
            'lab_order': forms.Select(attrs={'class': 'form-select'}),
            'consultation_charges': forms.NumberInput(attrs={'class': 'form-control fee-calc', 'step': '10'}),
            'lab_charges': forms.NumberInput(attrs={'class': 'form-control fee-calc', 'step': '10'}),
            'medicine_charges': forms.NumberInput(attrs={'class': 'form-control fee-calc', 'step': '10'}),
            'other_charges': forms.NumberInput(attrs={'class': 'form-control fee-calc', 'step': '10'}),
            'discount_amount': forms.NumberInput(attrs={'class': 'form-control fee-calc', 'step': '10'}),
            'tax_amount': forms.NumberInput(attrs={'class': 'form-control fee-calc', 'step': '10'}),
            'paid_amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '10'}),
            'payment_status': forms.Select(attrs={'class': 'form-select'}),
            'payment_method': forms.Select(attrs={'class': 'form-select'}),
            'transaction_reference': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. UPI Ref # 420912389123'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Payment remarks'}),
        }

class PaymentCollectionForm(forms.Form):
    payment_amount = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '10'})
    )
    payment_method = forms.ChoiceField(
        choices=Invoice.PAYMENT_METHOD,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    transaction_reference = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'UPI Ref / Card Approval Code'})
    )
    remarks = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Payment notes'})
    )
