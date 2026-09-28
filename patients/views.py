from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from accounts.decorators import staff_required
from .models import Patient
from .forms import PatientForm

@login_required
@staff_required
def patient_list(request):
    search_query = request.GET.get('search', '').strip()
    gender_filter = request.GET.get('gender', '')
    blood_filter = request.GET.get('blood_group', '')

    queryset = Patient.objects.all()

    if search_query:
        queryset = queryset.filter(
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(phone__icontains=search_query) |
            Q(email__icontains=search_query)
        )

    if gender_filter:
        queryset = queryset.filter(gender=gender_filter)
    if blood_filter:
        queryset = queryset.filter(blood_group=blood_filter)

    paginator = Paginator(queryset, 15)
    page_number = request.GET.get('page')
    patients = paginator.get_page(page_number)

    return render(request, 'patients/list.html', {
        'patients': patients,
        'search_query': search_query,
        'gender_filter': gender_filter,
        'blood_filter': blood_filter,
        'total_count': queryset.count(),
    })

@login_required
@staff_required
def patient_detail(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    appointments = patient.appointments.select_related('doctor__user').order_by('-appointment_date', '-appointment_time')
    lab_orders = patient.lab_orders.prefetch_related('items__test').order_by('-order_date')
    invoices = patient.invoices.order_by('-created_at')

    return render(request, 'patients/detail.html', {
        'patient': patient,
        'appointments': appointments,
        'lab_orders': lab_orders,
        'invoices': invoices,
    })

@login_required
@staff_required
def patient_create(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            patient = form.save()
            messages.success(request, f'Patient "{patient.full_name}" registered successfully.')
            return redirect('patient_detail', pk=patient.pk)
    else:
        form = PatientForm()

    return render(request, 'patients/form.html', {'form': form, 'title': 'Register New Patient'})

@login_required
@staff_required
def patient_edit(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    if request.method == 'POST':
        form = PatientForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()
            messages.success(request, f'Patient record for "{patient.full_name}" updated.')
            return redirect('patient_detail', pk=patient.pk)
    else:
        form = PatientForm(instance=patient)

    return render(request, 'patients/form.html', {'form': form, 'patient': patient, 'title': f'Edit Patient: {patient.full_name}'})

@login_required
@staff_required
def patient_delete(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    if request.method == 'POST':
        name = patient.full_name
        patient.delete()
        messages.warning(request, f'Patient "{name}" and associated records removed.')
        return redirect('patient_list')

    return render(request, 'patients/confirm_delete.html', {'patient': patient})
