from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from datetime import datetime
from doctors.models import Doctor
from lab.models import LabCategory, LabTest, LabOrder, LabOrderItem
from patients.models import Patient
from appointments.models import Appointment

def home(request):
    doctors = Doctor.objects.filter(is_available=True).select_related('user')[:6]
    lab_categories = LabCategory.objects.prefetch_related('tests').all()[:6]
    popular_tests = LabTest.objects.filter(is_active=True)[:8]

    return render(request, 'website/home.html', {
        'doctors': doctors,
        'lab_categories': lab_categories,
        'popular_tests': popular_tests,
    })

def about(request):
    doctors_count = Doctor.objects.filter(is_available=True).count()
    tests_count = LabTest.objects.filter(is_active=True).count()
    return render(request, 'website/about.html', {
        'doctors_count': doctors_count,
        'tests_count': tests_count,
    })

def medical_services(request):
    doctors = Doctor.objects.filter(is_available=True).select_related('user')
    return render(request, 'website/services.html', {'doctors': doctors})

def lab_services(request):
    categories = LabCategory.objects.prefetch_related('tests').all()
    all_tests = LabTest.objects.filter(is_active=True).select_related('category')
    return render(request, 'website/lab_services.html', {
        'categories': categories,
        'all_tests': all_tests,
    })

def doctor_profiles(request):
    doctors = Doctor.objects.filter(is_available=True).select_related('user')
    return render(request, 'website/doctors.html', {'doctors': doctors})

def timings(request):
    doctors = Doctor.objects.filter(is_available=True).select_related('user')
    return render(request, 'website/timings.html', {'doctors': doctors})

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        messages.success(request, f'Thank you {name}! Your message has been received. Our front desk will contact you shortly.')
        return redirect('contact')
    return render(request, 'website/contact.html')

def book_appointment(request):
    doctors = Doctor.objects.filter(is_available=True).select_related('user')
    
    if request.method == 'POST':
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        phone = request.POST.get('phone', '').strip()
        email = request.POST.get('email', '').strip()
        gender = request.POST.get('gender', 'other')
        dob_str = request.POST.get('date_of_birth', '')
        doctor_id = request.POST.get('doctor_id')
        appt_date_str = request.POST.get('appointment_date')
        appt_time_str = request.POST.get('appointment_time')
        reason = request.POST.get('reason', 'General Consultation')

        if not (first_name and phone and doctor_id and appt_date_str and appt_time_str):
            messages.error(request, 'Please complete all required fields.')
            return render(request, 'website/book_appointment.html', {'doctors': doctors})

        # Match or Create Patient
        patient = None
        if phone:
            patient = Patient.objects.filter(phone=phone).first()
        if not patient and email:
            patient = Patient.objects.filter(email=email).first()

        if not patient:
            # Create new patient record
            dob = None
            if dob_str:
                try:
                    dob = datetime.strptime(dob_str, '%Y-%m-%d').date()
                except ValueError:
                    dob = timezone.now().date()
            else:
                # Default age placeholder
                dob = timezone.now().date().replace(year=timezone.now().year - 30)

            patient = Patient.objects.create(
                first_name=first_name,
                last_name=last_name or 'Patient',
                phone=phone,
                email=email or f"{phone}@guest.royalcare.in",
                gender=gender,
                date_of_birth=dob,
            )

        doctor = get_object_or_404(Doctor, id=doctor_id)
        appt_date = datetime.strptime(appt_date_str, '%Y-%m-%d').date()
        appt_time = datetime.strptime(appt_time_str, '%H:%M').time()

        # Check for double booking
        conflict = Appointment.objects.filter(
            doctor=doctor,
            appointment_date=appt_date,
            appointment_time=appt_time,
            status__in=['scheduled', 'confirmed']
        ).exists()

        if conflict:
            messages.warning(request, f'Dr. {doctor.user.get_full_name()} is already booked at {appt_time_str} on {appt_date_str}. Please select an alternate slot.')
            return render(request, 'website/book_appointment.html', {'doctors': doctors})

        appointment = Appointment.objects.create(
            patient=patient,
            doctor=doctor,
            appointment_date=appt_date,
            appointment_time=appt_time,
            reason=reason,
            fee=doctor.consultation_fee,
            status='scheduled'
        )

        return render(request, 'website/booking_success.html', {
            'appointment': appointment,
            'patient': patient,
            'type': 'appointment',
        })

    return render(request, 'website/book_appointment.html', {'doctors': doctors})

def book_lab_test(request):
    tests = LabTest.objects.filter(is_active=True).select_related('category')
    
    if request.method == 'POST':
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        phone = request.POST.get('phone', '').strip()
        email = request.POST.get('email', '').strip()
        selected_tests = request.POST.getlist('tests')
        notes = request.POST.get('notes', '')

        if not (first_name and phone and selected_tests):
            messages.error(request, 'Please fill in your contact information and select at least one lab test.')
            return render(request, 'website/book_lab.html', {'tests': tests})

        patient = Patient.objects.filter(phone=phone).first()
        if not patient:
            patient = Patient.objects.create(
                first_name=first_name,
                last_name=last_name or 'Patient',
                phone=phone,
                email=email or f"{phone}@guest.royalcare.in",
                gender='other',
                date_of_birth=timezone.now().date().replace(year=timezone.now().year - 30)
            )

        order = LabOrder.objects.create(
            patient=patient,
            status='pending',
            notes=notes,
        )

        total = 0
        for test_id in selected_tests:
            test_obj = LabTest.objects.get(id=test_id)
            LabOrderItem.objects.create(
                order=order,
                test=test_obj,
                reference_range=test_obj.normal_range,
                unit=test_obj.unit
            )
            total += test_obj.price

        order.total_amount = total
        order.save()

        return render(request, 'website/booking_success.html', {
            'order': order,
            'patient': patient,
            'type': 'lab',
        })

    return render(request, 'website/book_lab.html', {'tests': tests})
