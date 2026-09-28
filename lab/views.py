from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.core.paginator import Paginator
from accounts.decorators import staff_required
from .models import LabCategory, LabTest, LabOrder, LabOrderItem
from .forms import LabOrderForm, LabTestForm

@login_required
@staff_required
def lab_dashboard(request):
    today = timezone.now().date()
    orders_today = LabOrder.objects.filter(order_date=today)
    
    total_orders = LabOrder.objects.count()
    pending_samples = LabOrder.objects.filter(status='pending').count()
    in_analysis = LabOrder.objects.filter(status='in_analysis').count()
    completed = LabOrder.objects.filter(status='completed').count()

    recent_orders = LabOrder.objects.select_related('patient', 'doctor__user').prefetch_related('items__test')[:10]
    categories = LabCategory.objects.prefetch_related('tests').all()

    return render(request, 'lab/dashboard.html', {
        'total_orders': total_orders,
        'pending_samples': pending_samples,
        'in_analysis': in_analysis,
        'completed': completed,
        'recent_orders': recent_orders,
        'categories': categories,
    })

@login_required
@staff_required
def test_catalog(request):
    category_id = request.GET.get('category')
    search = request.GET.get('search', '').strip()

    tests = LabTest.objects.select_related('category').all()
    if category_id:
        tests = tests.filter(category_id=category_id)
    if search:
        tests = tests.filter(name__icontains=search) | tests.filter(code__icontains=search)

    categories = LabCategory.objects.all()

    return render(request, 'lab/catalog.html', {
        'tests': tests,
        'categories': categories,
        'selected_category': category_id,
        'search': search,
    })

@login_required
@staff_required
def order_list(request):
    status_filter = request.GET.get('status', '')
    date_filter = request.GET.get('date', '')

    orders = LabOrder.objects.select_related('patient', 'doctor__user').all()
    if status_filter:
        orders = orders.filter(status=status_filter)
    if date_filter:
        orders = orders.filter(order_date=date_filter)

    paginator = Paginator(orders, 15)
    page = request.GET.get('page')
    orders_page = paginator.get_page(page)

    return render(request, 'lab/order_list.html', {
        'orders': orders_page,
        'status_filter': status_filter,
        'date_filter': date_filter,
    })

@login_required
@staff_required
def order_detail(request, pk):
    order = get_object_or_404(LabOrder.objects.select_related('patient', 'doctor__user').prefetch_related('items__test'), pk=pk)
    return render(request, 'lab/order_detail.html', {'order': order})

@login_required
@staff_required
def order_create(request):
    if request.method == 'POST':
        form = LabOrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.save()
            
            # Save selected tests
            tests = form.cleaned_data['tests']
            total = 0
            for t in tests:
                LabOrderItem.objects.create(
                    order=order,
                    test=t,
                    reference_range=t.normal_range,
                    unit=t.unit
                )
                total += t.price

            order.total_amount = total
            order.save()
            messages.success(request, f'Lab Order #{order.order_number} generated for {order.patient.full_name}.')
            return redirect('lab_order_detail', pk=order.pk)
    else:
        initial = {}
        patient_id = request.GET.get('patient_id')
        if patient_id:
            initial['patient'] = patient_id
        form = LabOrderForm(initial=initial)

    return render(request, 'lab/order_form.html', {'form': form, 'title': 'Create Diagnostic Lab Order'})

@login_required
@staff_required
def update_order_status(request, pk, new_status):
    order = get_object_or_404(LabOrder, pk=pk)
    if new_status in dict(LabOrder.STATUS_CHOICES).keys():
        order.status = new_status
        if new_status == 'sample_collected' and not order.sample_collected_at:
            order.sample_collected_at = timezone.now()
        elif new_status == 'completed' and not order.reported_at:
            order.reported_at = timezone.now()
        order.save()
        messages.success(request, f'Order #{order.order_number} status updated to {order.get_status_display()}.')
    return redirect('lab_order_detail', pk=order.pk)

@login_required
@staff_required
def enter_results(request, pk):
    order = get_object_or_404(LabOrder.objects.prefetch_related('items__test'), pk=pk)
    
    if request.method == 'POST':
        for item in order.items.all():
            val = request.POST.get(f'result_{item.id}', '')
            remarks = request.POST.get(f'remarks_{item.id}', '')
            abnormal = bool(request.POST.get(f'abnormal_{item.id}'))
            
            item.result_value = val
            item.technician_remarks = remarks
            item.is_abnormal = abnormal
            item.save()

        # Update order status to completed
        order.status = 'completed'
        order.reported_at = timezone.now()
        order.save()

        messages.success(request, f'Diagnostic test results saved and verified for {order.patient.full_name}.')
        return redirect('lab_order_detail', pk=order.pk)

    return render(request, 'lab/enter_results.html', {'order': order})

@login_required
@staff_required
def print_report(request, pk):
    order = get_object_or_404(LabOrder.objects.select_related('patient', 'doctor__user').prefetch_related('items__test'), pk=pk)
    return render(request, 'lab/report_print.html', {'order': order})
