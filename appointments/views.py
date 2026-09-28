from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from django.core.paginator import Paginator
from accounts.decorators import staff_required
from .models import Appointment
from .forms import AppointmentForm
from doctors.models import Doctor
from patients.models import Patient

@login_required
@staff_required
def appointment_list(request):
    date_filter = request.GET.get('date', '')
    status_filter = request.GET.get('status', '')
    doctor_filter = request.GET.get('doctor', '')

    queryset = Appointment.objects.select_related('patient', 'doctor__user').all()

    if date_filter:
        queryset = queryset.filter(appointment_date=date_filter)
    if status_filter:
        queryset = queryset.filter(status=status_filter)
    if doctor_filter:
        queryset = queryset.filter(doctor_id=doctor_filter)

    doctors = Doctor.objects.filter(is_available=True).select_related('user')
    
    paginator = Paginator(queryset, 15)
    page_number = request.GET.get('page')
    appointments = paginator.get_page(page_number)

    return render(request, 'appointments/list.html', {
        'appointments': appointments,
        'doctors': doctors,
        'date_filter': date_filter,
        'status_filter': status_filter,
        'doctor_filter': doctor_filter,
        'today': timezone.now().date(),
    })

@login_required
@staff_required
def appointment_detail(request, pk):
    appointment = get_object_or_404(
        Appointment.objects.select_related('patient', 'doctor__user'),
        pk=pk
    )
    prescription = getattr(appointment, 'prescription', None)
    invoice = getattr(appointment, 'invoice', None)

    return render(request, 'appointments/detail.html', {
        'appointment': appointment,
        'prescription': prescription,
        'invoice': invoice,
    })

@login_required
@staff_required
def appointment_create(request):
    initial_data = {}
    patient_id = request.GET.get('patient_id')
    if patient_id:
        initial_data['patient'] = patient_id

    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save()
            messages.success(request, f'Appointment booked successfully for {appointment.patient.full_name}.')
            return redirect('appointment_detail', pk=appointment.pk)
    else:
        form = AppointmentForm(initial=initial_data)

    return render(request, 'appointments/form.html', {'form': form, 'title': 'Book New Appointment'})

@login_required
@staff_required
def appointment_edit(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    if request.method == 'POST':
        form = AppointmentForm(request.POST, instance=appointment)
        if form.is_valid():
            appointment = form.save()
            messages.success(request, f'Appointment #{appointment.pk} updated successfully.')
            return redirect('appointment_detail', pk=appointment.pk)
    else:
        form = AppointmentForm(instance=appointment)

    return render(request, 'appointments/form.html', {'form': form, 'appointment': appointment, 'title': f'Edit Appointment #{appointment.pk}'})

@login_required
@staff_required
def appointment_status_update(request, pk, new_status):
    appointment = get_object_or_404(Appointment, pk=pk)
    valid_statuses = dict(Appointment.STATUS_CHOICES).keys()
    if new_status in valid_statuses:
        appointment.status = new_status
        appointment.save()
        messages.success(request, f'Appointment status changed to "{appointment.get_status_display()}".')
    else:
        messages.error(request, 'Invalid appointment status.')
    return redirect('appointment_detail', pk=appointment.pk)

def get_doctor_slots_api(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)
    date_str = request.GET.get('date', timezone.now().date().strftime('%Y-%m-%d'))
    
    all_slots = doctor.generate_time_slots()
    booked_slots = list(Appointment.objects.filter(
        doctor=doctor,
        appointment_date=date_str,
        status__in=['scheduled', 'confirmed', 'in_progress']
    ).values_list('appointment_time', flat=True))

    booked_formatted = [t.strftime('%H:%M') for t in booked_slots]

    available_slots = [
        {'time': s, 'available': s not in booked_formatted}
        for s in all_slots
    ]

    return JsonResponse({
        'doctor_id': doctor.id,
        'doctor_name': doctor.doctor_name,
        'fee': float(doctor.consultation_fee),
        'date': date_str,
        'slots': available_slots
    })
