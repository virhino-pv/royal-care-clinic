from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum
from django.core.paginator import Paginator
from accounts.decorators import staff_required
from .models import Invoice
from .forms import InvoiceForm, PaymentCollectionForm
from appointments.models import Appointment
from lab.models import LabOrder

@login_required
@staff_required
def invoice_list(request):
    status_filter = request.GET.get('status', '')
    method_filter = request.GET.get('method', '')
    search = request.GET.get('search', '').strip()

    invoices = Invoice.objects.select_related('patient', 'appointment', 'lab_order').all()

    if status_filter:
        invoices = invoices.filter(payment_status=status_filter)
    if method_filter:
        invoices = invoices.filter(payment_method=method_filter)
    if search:
        invoices = invoices.filter(
            invoice_number__icontains=search
        ) | invoices.filter(
            patient__first_name__icontains=search
        ) | invoices.filter(
            patient__phone__icontains=search
        )

    # Summary metrics
    total_billed = invoices.aggregate(total=Sum('total_amount'))['total'] or 0
    total_collected = invoices.aggregate(total=Sum('paid_amount'))['total'] or 0
    total_outstanding = max(0, total_billed - total_collected)

    paginator = Paginator(invoices, 15)
    page = request.GET.get('page')
    invoices_page = paginator.get_page(page)

    return render(request, 'billing/list.html', {
        'invoices': invoices_page,
        'status_filter': status_filter,
        'method_filter': method_filter,
        'search': search,
        'total_billed': total_billed,
        'total_collected': total_collected,
        'total_outstanding': total_outstanding,
    })

@login_required
@staff_required
def invoice_detail(request, pk):
    invoice = get_object_or_404(
        Invoice.objects.select_related('patient', 'appointment__doctor__user', 'lab_order'),
        pk=pk
    )
    payment_form = PaymentCollectionForm(initial={'payment_amount': invoice.balance_due})
    return render(request, 'billing/detail.html', {
        'invoice': invoice,
        'payment_form': payment_form,
    })

@login_required
@staff_required
def invoice_create(request):
    initial = {}
    patient_id = request.GET.get('patient_id')
    appointment_id = request.GET.get('appointment_id')
    lab_order_id = request.GET.get('lab_order_id')

    if patient_id:
        initial['patient'] = patient_id
    if appointment_id:
        appt = get_object_or_404(Appointment, pk=appointment_id)
        initial['appointment'] = appt
        initial['patient'] = appt.patient
        initial['consultation_charges'] = appt.fee
    if lab_order_id:
        order = get_object_or_404(LabOrder, pk=lab_order_id)
        initial['lab_order'] = order
        initial['patient'] = order.patient
        initial['lab_charges'] = order.total_amount

    if request.method == 'POST':
        form = InvoiceForm(request.POST)
        if form.is_valid():
            invoice = form.save()
            messages.success(request, f'Invoice #{invoice.invoice_number} created for {invoice.patient.full_name}.')
            return redirect('invoice_detail', pk=invoice.pk)
    else:
        form = InvoiceForm(initial=initial)

    return render(request, 'billing/form.html', {'form': form, 'title': 'Generate Healthcare Invoice'})

@login_required
@staff_required
def collect_payment(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    if request.method == 'POST':
        form = PaymentCollectionForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['payment_amount']
            method = form.cleaned_data['payment_method']
            ref = form.cleaned_data['transaction_reference']
            remarks = form.cleaned_data['remarks']

            invoice.paid_amount += amount
            invoice.payment_method = method
            if ref:
                invoice.transaction_reference = ref
            if remarks:
                invoice.notes = f"{invoice.notes}\n[Payment Note]: {remarks}".strip()
            invoice.save()

            messages.success(request, f'Payment of ₹{amount} recorded successfully for Invoice #{invoice.invoice_number}.')
    return redirect('invoice_detail', pk=invoice.pk)

@login_required
@staff_required
def invoice_print(request, pk):
    invoice = get_object_or_404(
        Invoice.objects.select_related('patient', 'appointment__doctor__user', 'lab_order'),
        pk=pk
    )
    return render(request, 'billing/print.html', {'invoice': invoice})
