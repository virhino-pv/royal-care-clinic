from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .forms import LoginForm, UserProfileForm
from .models import User

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.user
            login(request, user)
            messages.success(request, f'Welcome back, {user.get_full_name() or user.username}!')
            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)
            return redirect('dashboard')
    else:
        form = LoginForm()

    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out safely.')
    return redirect('home')

@login_required
def dashboard_view(request):
    user = request.user
    today = timezone.now().date()

    # Import models dynamically to prevent circular imports
    from patients.models import Patient
    from appointments.models import Appointment
    from lab.models import LabOrder
    from billing.models import Invoice

    # Metrics
    total_patients = Patient.objects.count()
    new_patients_today = Patient.objects.filter(created_at__date=today).count()
    
    today_appointments = Appointment.objects.filter(appointment_date=today)
    total_today_appointments = today_appointments.count()
    completed_today = today_appointments.filter(status='completed').count()
    pending_today = today_appointments.filter(status__in=['scheduled', 'confirmed']).count()

    today_lab_orders = LabOrder.objects.filter(order_date=today)
    total_today_lab = today_lab_orders.count()
    pending_lab = today_lab_orders.filter(status__in=['pending', 'sample_collected', 'in_analysis']).count()
    completed_lab = today_lab_orders.filter(status='completed').count()

    # Revenue
    from django.db.models import Sum
    today_revenue = Invoice.objects.filter(
        created_at__date=today,
        payment_status__in=['paid', 'partial']
    ).aggregate(total=Sum('paid_amount'))['total'] or 0

    recent_appointments = Appointment.objects.select_related('patient', 'doctor__user').order_by('-created_at')[:8]
    recent_lab_orders = LabOrder.objects.select_related('patient').order_by('-created_at')[:6]
    recent_invoices = Invoice.objects.select_related('patient').order_by('-created_at')[:6]

    context = {
        'total_patients': total_patients,
        'new_patients_today': new_patients_today,
        'total_today_appointments': total_today_appointments,
        'completed_today': completed_today,
        'pending_today': pending_today,
        'total_today_lab': total_today_lab,
        'pending_lab': pending_lab,
        'completed_lab': completed_lab,
        'today_revenue': today_revenue,
        'recent_appointments': recent_appointments,
        'recent_lab_orders': recent_lab_orders,
        'recent_invoices': recent_invoices,
        'today': today,
    }

    return render(request, 'dashboard/index.html', context)

@login_required
def profile_view(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully.')
            return redirect('profile')
    else:
        form = UserProfileForm(instance=request.user)

    return render(request, 'accounts/profile.html', {'form': form})
