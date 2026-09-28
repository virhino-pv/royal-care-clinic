from django import forms
from .models import Appointment
from doctors.models import Doctor

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = [
            'patient', 'doctor', 'appointment_date', 'appointment_time',
            'appointment_type', 'fee', 'status', 'reason', 'doctor_notes'
        ]
        widgets = {
            'patient': forms.Select(attrs={'class': 'form-select select2-enable'}),
            'doctor': forms.Select(attrs={'class': 'form-select'}),
            'appointment_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'appointment_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'appointment_type': forms.Select(attrs={'class': 'form-select'}),
            'fee': forms.NumberInput(attrs={'class': 'form-control', 'step': '50'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'reason': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Reason for appointment / chief complaints'}),
            'doctor_notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Clinical observations & private notes'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        doctor = cleaned_data.get('doctor')
        appt_date = cleaned_data.get('appointment_date')
        appt_time = cleaned_data.get('appointment_time')

        if doctor and appt_date and appt_time:
            qs = Appointment.objects.filter(
                doctor=doctor,
                appointment_date=appt_date,
                appointment_time=appt_time,
                status__in=['scheduled', 'confirmed', 'in_progress']
            )
            if self.instance and self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)

            if qs.exists():
                raise forms.ValidationError(
                    f"{doctor.doctor_name} already has an active appointment at {appt_time.strftime('%I:%M %p')} on {appt_date}. Please pick another time."
                )
        return cleaned_data
