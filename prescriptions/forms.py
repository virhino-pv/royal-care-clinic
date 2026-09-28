from django import forms
from django.forms import inlineformset_factory
from .models import Prescription, PrescriptionMedicine

class PrescriptionForm(forms.ModelForm):
    class Meta:
        model = Prescription
        fields = [
            'appointment', 'diagnosis', 'chief_complaints',
            'blood_pressure', 'pulse_rate', 'temperature', 'weight_kg',
            'advice_diet', 'follow_up_date'
        ]
        widgets = {
            'appointment': forms.Select(attrs={'class': 'form-select'}),
            'diagnosis': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'e.g. Acute Viral Bronchitis, Essential Hypertension'}),
            'chief_complaints': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Fever, cough, body pain since 3 days'}),
            'blood_pressure': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '120/80 mmHg'}),
            'pulse_rate': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '76 bpm'}),
            'temperature': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '98.6 F'}),
            'weight_kg': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1', 'placeholder': '65.5'}),
            'advice_diet': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Drink plenty of warm fluids, low salt diet, avoid cold items'}),
            'follow_up_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

class PrescriptionMedicineForm(forms.ModelForm):
    class Meta:
        model = PrescriptionMedicine
        fields = ['medicine_name', 'dosage', 'frequency', 'duration_days', 'instructions']
        widgets = {
            'medicine_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Medicine Name & Strength'}),
            'dosage': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '1 Tab / 5 ml'}),
            'frequency': forms.Select(attrs={'class': 'form-select'}),
            'duration_days': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'instructions': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'After food / with water'}),
        }

MedicineFormSet = inlineformset_factory(
    Prescription,
    PrescriptionMedicine,
    form=PrescriptionMedicineForm,
    extra=3,
    can_delete=True
)
