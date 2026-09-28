from django import forms
from .models import LabOrder, LabOrderItem, LabTest, LabCategory

class LabOrderForm(forms.ModelForm):
    tests = forms.ModelMultipleChoiceField(
        queryset=LabTest.objects.filter(is_active=True),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        required=True
    )

    class Meta:
        model = LabOrder
        fields = ['patient', 'doctor', 'priority', 'notes']
        widgets = {
            'patient': forms.Select(attrs={'class': 'form-select select2-enable'}),
            'doctor': forms.Select(attrs={'class': 'form-select'}),
            'priority': forms.Select(attrs={'class': 'form-select'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Clinical instructions or patient fasting status'}),
        }

class LabTestForm(forms.ModelForm):
    class Meta:
        model = LabTest
        fields = ['category', 'code', 'name', 'sample_type', 'price', 'turnaround_hours', 'normal_range', 'unit', 'description', 'is_active']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-select'}),
            'code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., CBC'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Complete Blood Count'}),
            'sample_type': forms.Select(attrs={'class': 'form-select'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '10'}),
            'turnaround_hours': forms.NumberInput(attrs={'class': 'form-control'}),
            'normal_range': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 12.0 - 16.0'}),
            'unit': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., g/dL'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
