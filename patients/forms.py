from django import forms
from .models import Patient

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = [
            'first_name', 'last_name', 'phone', 'email',
            'date_of_birth', 'gender', 'blood_group',
            'address', 'emergency_contact', 'allergies', 'medical_history'
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Mobile Number (e.g. 9840012345)'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'blood_group': forms.Select(attrs={'class': 'form-select'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Residential Address'}),
            'emergency_contact': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Contact Person Name & Phone'}),
            'allergies': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Penicillin, Dust, Sulfa drugs, etc.'}),
            'medical_history': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Known conditions: Diabetes, Hypertension, Asthma, etc.'}),
        }

    def clean_phone(self):
        phone = self.cleaned_data.get('phone', '').strip()
        if not Patient.validate_phone(phone):
            raise forms.ValidationError('Please enter a valid phone number with at least 10 digits.')
        
        # Unique check handling update
        instance = getattr(self, 'instance', None)
        qs = Patient.objects.filter(phone=phone)
        if instance and instance.pk:
            qs = qs.exclude(pk=instance.pk)
        if qs.exists():
            raise forms.ValidationError('A patient with this mobile number is already registered.')
        return phone
