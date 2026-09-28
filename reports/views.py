import io
import json
import zipfile
import pandas as pd
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from accounts.decorators import admin_required, staff_required
from .analytics import ClinicAnalyticsEngine
from patients.models import Patient
from appointments.models import Appointment
from billing.models import Invoice
from lab.models import LabOrder, LabTest

@login_required
@staff_required
def analytics_dashboard(request):
    summary = ClinicAnalyticsEngine.get_summary_metrics()
    appointment_trends = ClinicAnalyticsEngine.get_appointment_trends(days=14)
    peak_hours = ClinicAnalyticsEngine.get_peak_hours_distribution()
    doctor_perf = ClinicAnalyticsEngine.get_doctor_performance()
    monthly_rev = ClinicAnalyticsEngine.get_monthly_revenue_trends()
    payment_dist = ClinicAnalyticsEngine.get_payment_method_distribution()
    lab_demand = ClinicAnalyticsEngine.get_lab_test_demand()

    context = {
        'summary': summary,
        'doctor_perf': doctor_perf,
        'lab_demand': lab_demand,
        'appt_trends_json': json.dumps(appointment_trends),
        'peak_hours_json': json.dumps(peak_hours),
        'monthly_rev_json': json.dumps(monthly_rev),
        'payment_dist_json': json.dumps(payment_dist),
    }

    return render(request, 'reports/dashboard.html', context)

def _clean_df_for_excel(df):
    """Strip timezones from all datetime columns for Excel/OpenPyXL compatibility."""
    for col in df.columns:
        if pd.api.types.is_datetime64_any_dtype(df[col]):
            try:
                df[col] = df[col].dt.tz_localize(None)
            except (TypeError, AttributeError):
                pass
        elif col in ['created_at', 'updated_at', 'order_date', 'appointment_date', 'sample_collected_at', 'reported_at']:
            try:
                df[col] = pd.to_datetime(df[col]).dt.tz_localize(None).dt.strftime('%Y-%m-%d %H:%M:%S')
            except Exception:
                pass
    return df

@login_required
@admin_required
def export_excel_report(request):
    """
    Generates a professional multi-sheet Excel workbook using Pandas and openpyxl.
    """
    output = io.BytesIO()

    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        # Sheet 1: Executive Summary
        summary = ClinicAnalyticsEngine.get_summary_metrics()
        df_summary = pd.DataFrame(list(summary.items()), columns=['Metric', 'Value'])
        df_summary.to_excel(writer, sheet_name='Executive_Summary', index=False)

        # Sheet 2: Patients Master
        patients = list(Patient.objects.values(
            'id', 'first_name', 'last_name', 'phone', 'email', 'gender', 'blood_group',
            'date_of_birth', 'address', 'created_at'
        ))
        if patients:
            df_pat = pd.DataFrame(patients)
            df_pat = _clean_df_for_excel(df_pat)
            df_pat.to_excel(writer, sheet_name='Patients', index=False)

        # Sheet 3: Appointments
        appts = list(Appointment.objects.select_related('patient', 'doctor__user').values(
            'id', 'patient__first_name', 'patient__last_name', 'patient__phone',
            'doctor__user__first_name', 'doctor__user__last_name', 'doctor__specialization',
            'appointment_date', 'appointment_time', 'appointment_type', 'status', 'fee'
        ))
        if appts:
            df_appts = pd.DataFrame(appts)
            df_appts['appointment_time'] = df_appts['appointment_time'].astype(str)
            df_appts = _clean_df_for_excel(df_appts)
            df_appts.to_excel(writer, sheet_name='Appointments', index=False)

        # Sheet 4: Doctor Performance
        doctor_perf = ClinicAnalyticsEngine.get_doctor_performance()
        if doctor_perf:
            df_doc = pd.DataFrame(doctor_perf)
            df_doc.to_excel(writer, sheet_name='Doctor_Performance', index=False)

        # Sheet 5: Invoices & Revenue
        invs = list(Invoice.objects.select_related('patient').values(
            'invoice_number', 'patient__first_name', 'patient__last_name',
            'consultation_charges', 'lab_charges', 'medicine_charges', 'total_amount',
            'paid_amount', 'payment_status', 'payment_method', 'created_at'
        ))
        if invs:
            df_inv = pd.DataFrame(invs)
            for num_col in ['consultation_charges', 'lab_charges', 'medicine_charges', 'total_amount', 'paid_amount']:
                df_inv[num_col] = df_inv[num_col].astype(float)
            df_inv = _clean_df_for_excel(df_inv)
            df_inv.to_excel(writer, sheet_name='Invoices_Billing', index=False)

        # Sheet 6: Lab Test Demand
        lab_demand = ClinicAnalyticsEngine.get_lab_test_demand()
        if lab_demand:
            df_lab = pd.DataFrame(lab_demand)
            df_lab.to_excel(writer, sheet_name='Lab_Test_Demand', index=False)

    output.seek(0)

    filename = f"Royal_Care_Clinic_Analytics_Report_{pd.Timestamp.now().strftime('%Y%m%d')}.xlsx"
    response = HttpResponse(
        output.getvalue(),
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response

@login_required
@admin_required
def export_csv_report(request, dataset_name):
    """
    Exports individual clean CSV datasets.
    """
    datasets = ClinicAnalyticsEngine.generate_powerbi_datasets()
    
    if dataset_name in datasets:
        df = datasets[dataset_name]
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="RoyalCare_{dataset_name}.csv"'
        df.to_csv(response, index=False)
        return response
    else:
        return JsonResponse({'error': 'Dataset not found'}, status=404)

@login_required
@admin_required
def export_powerbi_bundle(request):
    """
    Packages all Star-Schema dimension and fact tables into a single ZIP bundle
    for seamless drag-and-drop into Microsoft Power BI Desktop.
    """
    datasets = ClinicAnalyticsEngine.generate_powerbi_datasets()
    
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for name, df in datasets.items():
            csv_data = df.to_csv(index=False)
            zip_file.writestr(f"{name}.csv", csv_data)

    zip_buffer.seek(0)
    response = HttpResponse(zip_buffer.getvalue(), content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename="RoyalCare_PowerBI_StarSchema_Datasets.zip"'
    return response
