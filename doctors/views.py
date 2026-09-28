from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from accounts.decorators import admin_required, staff_required
from accounts.models import User
from .models import Doctor
from .forms import DoctorForm

@login_required
@staff_required
def doctor_list(request):
    specialty_filter = request.GET.get('specialization', '')
    doctors = Doctor.objects.select_related('user').all()

    if specialty_filter:
        doctors = doctors.filter(specialization=specialty_filter)

    specialties = Doctor.SPECIALTY_CHOICES

    return render(request, 'doctors/list.html', {
        'doctors': doctors,
        'specialties': specialties,
        'selected_specialty': specialty_filter,
    })

@login_required
@staff_required
def doctor_detail(request, pk):
    doctor = get_object_or_404(Doctor.objects.select_related('user'), pk=pk)
    recent_appointments = doctor.appointments.select_related('patient').order_by('-appointment_date', '-appointment_time')[:10]
    return render(request, 'doctors/detail.html', {
        'doctor': doctor,
        'recent_appointments': recent_appointments,
    })

@login_required
@admin_required
def doctor_create(request):
    if request.method == 'POST':
        form = DoctorForm(request.POST, request.FILES)
        if form.is_valid():
            # Create underlying user account
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            username = email.split('@')[0] or f"dr_{first_name.lower()}"

            # Check if user exists
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    'first_name': first_name,
                    'last_name': last_name,
                    'email': email,
                    'phone': phone,
                    'role': 'doctor'
                }
            )
            if created:
                user.set_password('Doctor@1234')
                user.save()

            doctor = form.save(commit=False)
            doctor.user = user
            doctor.save()
            messages.success(request, f'Doctor profile for Dr. {user.get_full_name()} created successfully.')
            return redirect('doctor_detail', pk=doctor.pk)
    else:
        form = DoctorForm()

    return render(request, 'doctors/form.html', {'form': form, 'title': 'Add New Doctor'})

@login_required
@admin_required
def doctor_edit(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    if request.method == 'POST':
        form = DoctorForm(request.POST, request.FILES, instance=doctor)
        if form.is_valid():
            doctor = form.save()
            user = doctor.user
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.email = form.cleaned_data['email']
            user.phone = form.cleaned_data['phone']
            user.save()
            messages.success(request, f'Doctor profile for Dr. {user.get_full_name()} updated.')
            return redirect('doctor_detail', pk=doctor.pk)
    else:
        form = DoctorForm(instance=doctor)

    return render(request, 'doctors/form.html', {'form': form, 'doctor': doctor, 'title': f'Edit Dr. {doctor.user.get_full_name()}'})
