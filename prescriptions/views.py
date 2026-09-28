from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from accounts.decorators import staff_required, doctor_required
from appointments.models import Appointment
from .models import Prescription, PrescriptionMedicine
from .forms import PrescriptionForm, MedicineFormSet

@login_required
@staff_required
def prescription_list(request):
    search = request.GET.get('search', '').strip()
    prescriptions = Prescription.objects.select_related(
        'appointment__patient', 'appointment__doctor__user'
    ).all()

    if request.user.is_doctor and not (request.user.is_admin or request.user.is_superuser):
        prescriptions = prescriptions.filter(appointment__doctor__user=request.user)

    if search:
        prescriptions = prescriptions.filter(
            appointment__patient__first_name__icontains=search
        ) | prescriptions.filter(
            appointment__patient__phone__icontains=search
        ) | prescriptions.filter(
            diagnosis__icontains=search
        )

    return render(request, 'prescriptions/list.html', {
        'prescriptions': prescriptions,
        'search': search,
    })

@login_required
@staff_required
def prescription_detail(request, pk):
    prescription = get_object_or_404(
        Prescription.objects.select_related(
            'appointment__patient', 'appointment__doctor__user'
        ).prefetch_related('medicines'),
        pk=pk
    )
    return render(request, 'prescriptions/detail.html', {'prescription': prescription})

@login_required
@doctor_required
def prescription_create(request, appointment_id):
    appointment = get_object_or_404(Appointment, pk=appointment_id)
    
    # Check if prescription already exists
    if hasattr(appointment, 'prescription'):
        messages.info(request, 'Prescription already exists for this appointment.')
        return redirect('prescription_detail', pk=appointment.prescription.pk)

    if request.method == 'POST':
        form = PrescriptionForm(request.POST)
        formset = MedicineFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            prescription = form.save()
            formset.instance = prescription
            formset.save()
            
            # Auto mark appointment completed
            appointment.status = 'completed'
            appointment.save()

            messages.success(request, f'Prescription created for {appointment.patient.full_name}.')
            return redirect('prescription_detail', pk=prescription.pk)
    else:
        form = PrescriptionForm(initial={'appointment': appointment})
        formset = MedicineFormSet()

    return render(request, 'prescriptions/form.html', {
        'form': form,
        'formset': formset,
        'appointment': appointment,
        'title': f'Write Prescription — {appointment.patient.full_name}',
    })

@login_required
@staff_required
def prescription_print(request, pk):
    prescription = get_object_or_404(
        Prescription.objects.select_related(
            'appointment__patient', 'appointment__doctor__user'
        ).prefetch_related('medicines'),
        pk=pk
    )
    return render(request, 'prescriptions/print.html', {'prescription': prescription})
