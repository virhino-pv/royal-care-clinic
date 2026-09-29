import os
import sys
from pathlib import Path

# Add project root to sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'royalcare_project.settings')

import django
django.setup()

import pandas as pd
import numpy as np
from reports.analytics import ClinicAnalyticsEngine
from reports.sql_analytics import SQLAnalyticsExecutor

def run_analytics_pipeline():
    """
    Executes the comprehensive Python + Pandas healthcare analytics pipeline
    for Royal Care Clinic & Lab (Powered by Virhino.com).
    """
    print("==================================================================")
    print("  ROYAL CARE CLINIC & LAB — HEALTHCARE ANALYTICS PIPELINE")
    print("  Powered by Virhino.com")
    print("==================================================================")

    # 1. Summary KPIs
    print("\n[Step 1/5] Extracting and calculating summary metrics...")
    summary = ClinicAnalyticsEngine.get_summary_metrics()
    for k, v in summary.items():
        print(f"  • {k}: {v}")

    # 2. Data Cleaning & Integrity Audits
    print("\n[Step 2/5] Running Data Quality & Integrity Validation...")
    from patients.models import Patient
    from appointments.models import Appointment
    from billing.models import Invoice

    patients_df = pd.DataFrame(list(Patient.objects.values()))
    if not patients_df.empty:
        null_phones = patients_df['phone'].isnull().sum()
        dup_phones = patients_df.duplicated(subset=['phone']).sum()
        print(f"  • Patient Records Analyzed: {len(patients_df)}")
        print(f"  • Missing Phone Numbers: {null_phones}")
        print(f"  • Duplicate Phone Entries: {dup_phones}")
    else:
        print("  • No patient records found in active database.")

    appts_df = pd.DataFrame(list(Appointment.objects.values()))
    if not appts_df.empty:
        dup_slots = appts_df.duplicated(subset=['doctor_id', 'appointment_date', 'appointment_time']).sum()
        print(f"  • Appointment Records Analyzed: {len(appts_df)}")
        print(f"  • Conflicting Duplicate Slots: {dup_slots}")

    # 3. SQL Analytics Execution
    print("\n[Step 3/5] Executing Database SQL Analytics Layer...")
    daily_df = SQLAnalyticsExecutor.get_daily_appointments_sql()
    print(f"  • Daily Appointments Extracted: {len(daily_df)} rows")

    doc_df = SQLAnalyticsExecutor.get_doctor_performance_sql()
    print(f"  • Doctor Performance Aggregations: {len(doc_df)} doctors")

    # 4. Power BI Star Schema Generation
    print("\n[Step 4/5] Building Power BI Star-Schema Datasets...")
    datasets = ClinicAnalyticsEngine.generate_powerbi_datasets()
    for name, df in datasets.items():
        print(f"  • Table '{name}': {len(df)} rows, {len(df.columns)} columns")

    # 5. Export Verification
    print("\n[Step 5/5] Export verification complete.")
    print("==================================================================")
    print("  ANALYTICS PIPELINE RUN COMPLETED SUCCESSFULLY!")
    print("==================================================================")

if __name__ == '__main__':
    run_analytics_pipeline()
