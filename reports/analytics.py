import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from django.utils import timezone
from patients.models import Patient
from doctors.models import Doctor
from appointments.models import Appointment
from lab.models import LabOrder, LabOrderItem, LabTest
from billing.models import Invoice

class ClinicAnalyticsEngine:
    """
    Python + Pandas Powered Healthcare Analytics Engine for Royal Care Clinic & Lab.
    Provides statistical summaries, cohort analysis, and Power BI dimensional models.
    """

    @staticmethod
    def get_summary_metrics():
        today = timezone.now().date()
        thirty_days_ago = today - timedelta(days=30)

        # 1. Patients Summary
        total_patients = Patient.objects.count()
        new_patients_30d = Patient.objects.filter(created_at__date__gte=thirty_days_ago).count()
        
        # Calculate returning patients using Pandas
        all_appts = list(Appointment.objects.values('patient_id', 'id'))
        if all_appts:
            df_appts = pd.DataFrame(all_appts)
            patient_visit_counts = df_appts.groupby('patient_id').size()
            returning_patients_count = int((patient_visit_counts > 1).sum())
        else:
            returning_patients_count = 0

        # 2. Appointments Summary
        total_appointments = Appointment.objects.count()
        completed_appointments = Appointment.objects.filter(status='completed').count()
        cancelled_appointments = Appointment.objects.filter(status='cancelled').count()
        no_show_appointments = Appointment.objects.filter(status='no_show').count()
        scheduled_appointments = Appointment.objects.filter(status__in=['scheduled', 'confirmed']).count()

        completion_rate = round((completed_appointments / total_appointments * 100), 1) if total_appointments > 0 else 0
        no_show_rate = round((no_show_appointments / total_appointments * 100), 1) if total_appointments > 0 else 0

        # 3. Revenue Summary
        invoices_qs = list(Invoice.objects.values(
            'total_amount', 'paid_amount', 'payment_status', 'payment_method',
            'consultation_charges', 'lab_charges', 'medicine_charges', 'created_at'
        ))
        
        if invoices_qs:
            df_inv = pd.DataFrame(invoices_qs)
            df_inv['total_amount'] = df_inv['total_amount'].astype(float)
            df_inv['paid_amount'] = df_inv['paid_amount'].astype(float)
            
            total_revenue = float(df_inv['paid_amount'].sum())
            total_billed = float(df_inv['total_amount'].sum())
            total_outstanding = max(0.0, total_billed - total_revenue)
        else:
            total_revenue = 0.0
            total_billed = 0.0
            total_outstanding = 0.0

        # 4. Lab Tests Summary
        total_lab_orders = LabOrder.objects.count()
        total_tests_conducted = LabOrderItem.objects.count()

        return {
            'total_patients': total_patients,
            'new_patients_30d': new_patients_30d,
            'returning_patients': returning_patients_count,
            'new_vs_returning_ratio': round((returning_patients_count / total_patients * 100), 1) if total_patients > 0 else 0,
            
            'total_appointments': total_appointments,
            'completed_appointments': completed_appointments,
            'cancelled_appointments': cancelled_appointments,
            'no_show_appointments': no_show_appointments,
            'scheduled_appointments': scheduled_appointments,
            'completion_rate': completion_rate,
            'no_show_rate': no_show_rate,

            'total_revenue': total_revenue,
            'total_billed': total_billed,
            'total_outstanding': total_outstanding,

            'total_lab_orders': total_lab_orders,
            'total_tests_conducted': total_tests_conducted,
        }

    @staticmethod
    def get_appointment_trends(days=30):
        start_date = timezone.now().date() - timedelta(days=days)
        appts = list(Appointment.objects.filter(appointment_date__gte=start_date).values('appointment_date', 'status'))
        
        if not appts:
            return {'dates': [], 'completed': [], 'cancelled': [], 'total': []}

        df = pd.DataFrame(appts)
        df['appointment_date'] = pd.to_datetime(df['appointment_date']).dt.strftime('%Y-%m-%d')
        
        # Group by date and status
        pivot = pd.crosstab(df['appointment_date'], df['status']).reset_index()
        
        dates = pivot['appointment_date'].tolist()
        completed = pivot['completed'].tolist() if 'completed' in pivot.columns else [0] * len(dates)
        cancelled = pivot['cancelled'].tolist() if 'cancelled' in pivot.columns else [0] * len(dates)
        total = df.groupby('appointment_date').size().reindex(dates, fill_value=0).tolist()

        return {
            'dates': dates,
            'completed': completed,
            'cancelled': cancelled,
            'total': total,
        }

    @staticmethod
    def get_peak_hours_distribution():
        appts = list(Appointment.objects.values('appointment_time'))
        if not appts:
            return {'hours': [f"{h}:00" for h in range(8, 21)], 'counts': [0] * 13}

        df = pd.DataFrame(appts)
        df['hour'] = df['appointment_time'].apply(lambda t: t.hour)
        
        hour_counts = df['hour'].value_counts().sort_index()
        
        all_hours = list(range(8, 21))
        counts = [int(hour_counts.get(h, 0)) for h in all_hours]
        labels = [f"{h:02d}:00" for h in all_hours]

        return {
            'hours': labels,
            'counts': counts,
        }

    @staticmethod
    def get_doctor_performance():
        appts = list(Appointment.objects.select_related('doctor__user').values(
            'doctor__user__first_name', 'doctor__user__last_name',
            'doctor__specialization', 'status', 'fee'
        ))
        if not appts:
            return []

        df = pd.DataFrame(appts)
        df['doctor_name'] = 'Dr. ' + df['doctor__user__first_name'].fillna('') + ' ' + df['doctor__user__last_name'].fillna('')
        df['doctor_name'] = df['doctor_name'].str.strip()
        df['fee'] = df['fee'].astype(float)

        stats = []
        for name, group in df.groupby('doctor_name'):
            specialty = group['doctor__specialization'].iloc[0]
            total_appts = len(group)
            completed = (group['status'] == 'completed').sum()
            cancelled = (group['status'] == 'cancelled').sum()
            no_show = (group['status'] == 'no_show').sum()
            revenue_generated = group[group['status'] == 'completed']['fee'].sum()

            stats.append({
                'doctor_name': name,
                'specialty': specialty,
                'total_appointments': int(total_appts),
                'completed': int(completed),
                'cancelled': int(cancelled),
                'no_show': int(no_show),
                'revenue': float(revenue_generated),
                'completion_pct': round(completed / total_appts * 100, 1) if total_appts > 0 else 0
            })

        # Sort by total appointments descending
        stats.sort(key=lambda x: x['total_appointments'], reverse=True)
        return stats

    @staticmethod
    def get_monthly_revenue_trends():
        invoices = list(Invoice.objects.values('created_at', 'paid_amount', 'consultation_charges', 'lab_charges'))
        if not invoices:
            return {'months': [], 'revenue': [], 'consultation': [], 'lab': []}

        df = pd.DataFrame(invoices)
        df['month'] = pd.to_datetime(df['created_at']).dt.strftime('%b %Y')
        df['paid_amount'] = df['paid_amount'].astype(float)
        df['consultation_charges'] = df['consultation_charges'].astype(float)
        df['lab_charges'] = df['lab_charges'].astype(float)

        grouped = df.groupby('month', sort=False).agg({
            'paid_amount': 'sum',
            'consultation_charges': 'sum',
            'lab_charges': 'sum'
        }).reset_index()

        return {
            'months': grouped['month'].tolist(),
            'revenue': grouped['paid_amount'].tolist(),
            'consultation': grouped['consultation_charges'].tolist(),
            'lab': grouped['lab_charges'].tolist(),
        }

    @staticmethod
    def get_payment_method_distribution():
        invoices = list(Invoice.objects.filter(paid_amount__gt=0).values('payment_method', 'paid_amount'))
        if not invoices:
            return {'methods': ['Cash', 'UPI / QR', 'Card', 'Net Banking'], 'amounts': [0, 0, 0, 0]}

        df = pd.DataFrame(invoices)
        df['paid_amount'] = df['paid_amount'].astype(float)
        
        method_map = {
            'cash': 'Cash Payment',
            'upi': 'UPI / QR Code',
            'card': 'Credit / Debit Card',
            'net_banking': 'Net Banking'
        }
        df['payment_method'] = df['payment_method'].map(lambda m: method_map.get(m, m.title()))

        grouped = df.groupby('payment_method')['paid_amount'].sum().reset_index()
        return {
            'methods': grouped['payment_method'].tolist(),
            'amounts': grouped['paid_amount'].tolist(),
        }

    @staticmethod
    def get_lab_test_demand():
        items = list(LabOrderItem.objects.select_related('test__category').values(
            'test__name', 'test__code', 'test__category__name', 'test__price'
        ))
        if not items:
            return []

        df = pd.DataFrame(items)
        df['test__price'] = df['test__price'].astype(float)

        demand = []
        for (name, code, cat), group in df.groupby(['test__name', 'test__code', 'test__category__name']):
            count = len(group)
            total_rev = group['test__price'].sum()
            demand.append({
                'test_name': name,
                'code': code,
                'category': cat,
                'order_count': int(count),
                'total_revenue': float(total_rev),
            })

        demand.sort(key=lambda x: x['order_count'], reverse=True)
        return demand

    # =======================================================
    # POWER BI STAR-SCHEMA DATASET GENERATORS
    # =======================================================
    @staticmethod
    def generate_powerbi_datasets():
        """
        Builds clean, denormalized Fact and Dimension DataFrames
        ideal for direct ingestion into Microsoft Power BI Desktop / Service.
        """
        # DimDate
        date_range = pd.date_range(start='2025-01-01', end='2027-12-31', freq='D')
        dim_date = pd.DataFrame({
            'DateKey': date_range.strftime('%Y%m%d').astype(int),
            'FullDate': date_range.strftime('%Y-%m-%d'),
            'Year': date_range.year,
            'Quarter': 'Q' + date_range.quarter.astype(str),
            'Month': date_range.month,
            'MonthName': date_range.strftime('%B'),
            'DayOfWeek': date_range.strftime('%A'),
            'IsWeekend': date_range.dayofweek.isin([5, 6]),
        })

        # DimPatient
        patients = list(Patient.objects.values(
            'id', 'first_name', 'last_name', 'phone', 'email', 'gender',
            'blood_group', 'date_of_birth', 'created_at'
        ))
        dim_patient = pd.DataFrame(patients)
        if not dim_patient.empty:
            dim_patient['FullName'] = dim_patient['first_name'] + ' ' + dim_patient['last_name'].fillna('')
            dim_patient['CreatedDate'] = pd.to_datetime(dim_patient['created_at']).dt.strftime('%Y-%m-%d')
            dim_patient.rename(columns={'id': 'PatientKey'}, inplace=True)
        else:
            dim_patient = pd.DataFrame(columns=['PatientKey', 'FullName', 'phone', 'gender', 'blood_group', 'CreatedDate'])

        # DimDoctor
        doctors = list(Doctor.objects.select_related('user').values(
            'id', 'user__first_name', 'user__last_name', 'specialization',
            'qualification', 'experience_years', 'consultation_fee', 'room_number'
        ))
        dim_doctor = pd.DataFrame(doctors)
        if not dim_doctor.empty:
            dim_doctor['DoctorName'] = 'Dr. ' + dim_doctor['user__first_name'] + ' ' + dim_doctor['user__last_name'].fillna('')
            dim_doctor.rename(columns={'id': 'DoctorKey', 'specialization': 'Specialty'}, inplace=True)
        else:
            dim_doctor = pd.DataFrame(columns=['DoctorKey', 'DoctorName', 'Specialty', 'qualification', 'consultation_fee'])

        # DimLabTest
        tests = list(LabTest.objects.select_related('category').values(
            'id', 'code', 'name', 'category__name', 'sample_type', 'price', 'turnaround_hours'
        ))
        dim_test = pd.DataFrame(tests)
        if not dim_test.empty:
            dim_test.rename(columns={'id': 'TestKey', 'category__name': 'Category', 'name': 'TestName'}, inplace=True)
        else:
            dim_test = pd.DataFrame(columns=['TestKey', 'code', 'TestName', 'Category', 'price'])

        # FactAppointments
        appts = list(Appointment.objects.values(
            'id', 'patient_id', 'doctor_id', 'appointment_date', 'appointment_time',
            'appointment_type', 'status', 'fee'
        ))
        fact_appts = pd.DataFrame(appts)
        if not fact_appts.empty:
            fact_appts['DateKey'] = pd.to_datetime(fact_appts['appointment_date']).dt.strftime('%Y%m%d').astype(int)
            fact_appts['Hour'] = fact_appts['appointment_time'].apply(lambda t: t.hour)
            fact_appts['Fee'] = fact_appts['fee'].astype(float)
            fact_appts.rename(columns={'id': 'AppointmentKey', 'patient_id': 'PatientKey', 'doctor_id': 'DoctorKey'}, inplace=True)
        else:
            fact_appts = pd.DataFrame(columns=['AppointmentKey', 'PatientKey', 'DoctorKey', 'DateKey', 'Hour', 'status', 'Fee'])

        # FactBilling
        invs = list(Invoice.objects.values(
            'id', 'invoice_number', 'patient_id', 'appointment_id', 'lab_order_id',
            'consultation_charges', 'lab_charges', 'medicine_charges', 'discount_amount',
            'tax_amount', 'total_amount', 'paid_amount', 'payment_status', 'payment_method',
            'created_at'
        ))
        fact_billing = pd.DataFrame(invs)
        if not fact_billing.empty:
            fact_billing['DateKey'] = pd.to_datetime(fact_billing['created_at']).dt.strftime('%Y%m%d').astype(int)
            for col in ['consultation_charges', 'lab_charges', 'medicine_charges', 'discount_amount', 'tax_amount', 'total_amount', 'paid_amount']:
                fact_billing[col] = fact_billing[col].astype(float)
            fact_billing.rename(columns={'id': 'InvoiceKey', 'patient_id': 'PatientKey'}, inplace=True)
        else:
            fact_billing = pd.DataFrame(columns=['InvoiceKey', 'PatientKey', 'DateKey', 'total_amount', 'paid_amount', 'payment_status', 'payment_method'])

        # FactLabOrders
        lab_items = list(LabOrderItem.objects.select_related('order').values(
            'id', 'order__id', 'order__patient_id', 'order__doctor_id', 'test_id',
            'order__order_date', 'order__status', 'order__priority', 'is_abnormal', 'test__price'
        ))
        fact_lab = pd.DataFrame(lab_items)
        if not fact_lab.empty:
            fact_lab['DateKey'] = pd.to_datetime(fact_lab['order__order_date']).dt.strftime('%Y%m%d').astype(int)
            fact_lab['Price'] = fact_lab['test__price'].astype(float)
            fact_lab.rename(columns={
                'id': 'OrderItemKey',
                'order__id': 'OrderKey',
                'order__patient_id': 'PatientKey',
                'order__doctor_id': 'DoctorKey',
                'test_id': 'TestKey',
                'order__status': 'Status',
                'order__priority': 'Priority',
            }, inplace=True)
        else:
            fact_lab = pd.DataFrame(columns=['OrderItemKey', 'OrderKey', 'PatientKey', 'TestKey', 'DateKey', 'Price', 'Status'])

        return {
            'DimDate': dim_date,
            'DimPatient': dim_patient,
            'DimDoctor': dim_doctor,
            'DimLabTest': dim_test,
            'FactAppointments': fact_appts,
            'FactBilling': fact_billing,
            'FactLabOrders': fact_lab,
        }
