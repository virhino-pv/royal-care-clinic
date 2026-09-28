from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import datetime, timedelta, date, time
from decimal import Decimal
import random

from accounts.models import User
from patients.models import Patient
from doctors.models import Doctor
from appointments.models import Appointment
from lab.models import LabCategory, LabTest, LabOrder, LabOrderItem
from prescriptions.models import Prescription, PrescriptionMedicine
from billing.models import Invoice

class Command(BaseCommand):
    help = 'Seeds initial demographic, clinical, diagnostic, and billing records for Royal Care Clinic & Lab.'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.NOTICE('Beginning seeding for Royal Care Clinic & Lab...'))

        # 1. Staff Users
        admin_user, _ = User.objects.get_or_create(
            username='admin',
            defaults={
                'first_name': 'Medical',
                'last_name': 'Director',
                'email': 'admin@royalcareclinic.in',
                'phone': '+91 98400 12345',
                'role': 'admin',
                'is_staff': True,
                'is_superuser': True,
            }
        )
        admin_user.set_password('admin123')
        admin_user.save()

        receptionist_user, _ = User.objects.get_or_create(
            username='receptionist',
            defaults={
                'first_name': 'Priya',
                'last_name': 'Sundaram',
                'email': 'frontdesk@royalcareclinic.in',
                'phone': '+91 98400 22334',
                'role': 'receptionist',
                'is_staff': True,
            }
        )
        receptionist_user.set_password('Staff@1234')
        receptionist_user.save()

        lab_tech_user, _ = User.objects.get_or_create(
            username='lab_tech',
            defaults={
                'first_name': 'Karthik',
                'last_name': 'Ramasamy',
                'email': 'lab@royalcareclinic.in',
                'phone': '+91 98400 33445',
                'role': 'lab_technician',
                'is_staff': True,
            }
        )
        lab_tech_user.set_password('Lab@1234')
        lab_tech_user.save()

        # 2. Doctors & Accounts
        doctors_data = [
            {
                'username': 'dr_sharma',
                'first_name': 'Ananya',
                'last_name': 'Sharma',
                'email': 'dr.ananya@royalcareclinic.in',
                'phone': '+91 98400 55661',
                'specialization': 'General Physician',
                'qualification': 'MBBS, MD (General Medicine)',
                'experience': 12,
                'fee': Decimal('400.00'),
                'room': 'OPD-1',
                'start': time(8, 0),
                'end': time(14, 0),
                'days': 'Monday,Tuesday,Wednesday,Thursday,Friday,Saturday',
            },
            {
                'username': 'dr_rajesh',
                'first_name': 'Rajesh',
                'last_name': 'Kannan',
                'email': 'dr.rajesh@royalcareclinic.in',
                'phone': '+91 98400 55662',
                'specialization': 'Cardiologist',
                'qualification': 'MBBS, MD, DM (Cardiology), FACC',
                'experience': 15,
                'fee': Decimal('700.00'),
                'room': 'OPD-2',
                'start': time(16, 0),
                'end': time(20, 30),
                'days': 'Monday,Wednesday,Friday',
            },
            {
                'username': 'dr_radhika',
                'first_name': 'Radhika',
                'last_name': 'Venkatesh',
                'email': 'dr.radhika@royalcareclinic.in',
                'phone': '+91 98400 55663',
                'specialization': 'Diabetologist',
                'qualification': 'MBBS, MD, Fellowship in Diabetology (UK)',
                'experience': 10,
                'fee': Decimal('500.00'),
                'room': 'OPD-3',
                'start': time(9, 0),
                'end': time(13, 30),
                'days': 'Tuesday,Thursday,Saturday',
            },
            {
                'username': 'dr_meera',
                'first_name': 'Meera',
                'last_name': 'Natarajan',
                'email': 'dr.meera@royalcareclinic.in',
                'phone': '+91 98400 55664',
                'specialization': 'Pediatrician',
                'qualification': 'MBBS, DCH, DNB (Pediatrics)',
                'experience': 9,
                'fee': Decimal('450.00'),
                'room': 'OPD-4',
                'start': time(10, 0),
                'end': time(17, 0),
                'days': 'Monday,Tuesday,Wednesday,Thursday,Friday,Saturday',
            },
            {
                'username': 'dr_kavitha',
                'first_name': 'Kavitha',
                'last_name': 'Balaji',
                'email': 'dr.kavitha@royalcareclinic.in',
                'phone': '+91 98400 55665',
                'specialization': 'Gynecologist',
                'qualification': 'MBBS, MS (OBG), FMAS',
                'experience': 14,
                'fee': Decimal('600.00'),
                'room': 'OPD-5',
                'start': time(15, 0),
                'end': time(19, 30),
                'days': 'Monday,Tuesday,Thursday,Friday',
            },
            {
                'username': 'dr_suresh',
                'first_name': 'Suresh',
                'last_name': 'Chandran',
                'email': 'dr.suresh@royalcareclinic.in',
                'phone': '+91 98400 55666',
                'specialization': 'Dermatologist',
                'qualification': 'MBBS, MD (DVL)',
                'experience': 8,
                'fee': Decimal('500.00'),
                'room': 'OPD-6',
                'start': time(17, 30),
                'end': time(21, 0),
                'days': 'Monday,Wednesday,Saturday',
            },
        ]

        created_doctors = []
        for d in doctors_data:
            doc_user, _ = User.objects.get_or_create(
                username=d['username'],
                defaults={
                    'first_name': d['first_name'],
                    'last_name': d['last_name'],
                    'email': d['email'],
                    'phone': d['phone'],
                    'role': 'doctor',
                    'is_staff': True,
                }
            )
            doc_user.set_password('Doctor@1234')
            doc_user.save()

            doc_obj, _ = Doctor.objects.get_or_create(
                user=doc_user,
                defaults={
                    'specialization': d['specialization'],
                    'qualification': d['qualification'],
                    'experience_years': d['experience'],
                    'consultation_fee': d['fee'],
                    'room_number': d['room'],
                    'start_time': d['start'],
                    'end_time': d['end'],
                    'available_days': d['days'],
                    'is_available': True,
                }
            )
            created_doctors.append(doc_obj)

        # 3. Diagnostic Categories & Tests
        lab_data = {
            'Hematology': [
                ('CBC', 'Complete Blood Count (CBC with ESR)', 'Blood', Decimal('350.00'), 2, 'Hb: 12.0 - 16.0', 'g/dL', 'Measures RBC, WBC, Platelets, Hematocrit, and differential.'),
                ('HB', 'Hemoglobin (Hb Estimation)', 'Blood', Decimal('120.00'), 1, '12.0 - 16.5', 'g/dL', 'Screening for anemia and blood loss.'),
                ('ESR', 'Erythrocyte Sedimentation Rate (ESR)', 'Blood', Decimal('100.00'), 1, '0 - 20', 'mm/hr', 'Inflammatory indicator.'),
                ('BT_CT', 'Bleeding Time & Clotting Time', 'Blood', Decimal('150.00'), 1, 'BT: 1-5 min, CT: 3-8 min', 'mins', 'Pre-operative coagulation assessment.'),
            ],
            'Biochemistry & Diabetes': [
                ('FBS', 'Fasting Blood Sugar (FBS)', 'Blood', Decimal('90.00'), 1, '70 - 100', 'mg/dL', 'Fasting glucose evaluation for diabetes mellitus.'),
                ('PPBS', 'Post Prandial Blood Sugar (PPBS)', 'Blood', Decimal('90.00'), 1, '< 140', 'mg/dL', 'Post-meal glycemic control.'),
                ('HBA1C', 'Glycated Hemoglobin (HbA1c)', 'Blood', Decimal('450.00'), 3, '< 5.7 (Normal), 5.7-6.4 (Prediabetes)', '%', '3-month average blood glucose level.'),
                ('LIPID', 'Complete Lipid Profile', 'Blood', Decimal('650.00'), 4, 'Total Chol: < 200, HDL: > 40, LDL: < 100', 'mg/dL', 'Cardiovascular lipid risk evaluation.'),
                ('LFT', 'Liver Function Test (LFT Profile)', 'Blood', Decimal('750.00'), 4, 'SGOT: < 35, SGPT: < 45, Bilirubin: 0.2-1.2', 'U/L', 'Comprehensive hepatic enzyme panel.'),
                ('KFT', 'Kidney Function Test / Renal Panel', 'Blood', Decimal('600.00'), 3, 'Urea: 15-40, Creatinine: 0.6-1.2, Uric Acid: 3.5-7.2', 'mg/dL', 'Renal clearance and glomerular health.'),
            ],
            'Thyroid & Hormones': [
                ('TSH', 'Thyroid Stimulating Hormone (Ultra TSH)', 'Blood', Decimal('250.00'), 3, '0.4 - 4.5', 'μIU/mL', 'Screening for hypothyroidism and hyperthyroidism.'),
                ('THYROID_TOTAL', 'Complete Thyroid Profile (T3, T4, TSH)', 'Blood', Decimal('550.00'), 4, 'T3: 0.8-2.0, T4: 5.1-14.1, TSH: 0.4-4.5', 'ng/mL', 'Full hormonal thyroid panel.'),
                ('VIT_D', 'Vitamin D (25-Hydroxy)', 'Blood', Decimal('950.00'), 6, '30 - 100', 'ng/mL', 'Bone density and immune regulatory vitamin level.'),
                ('VIT_B12', 'Vitamin B12 (Cyanocobalamin)', 'Blood', Decimal('800.00'), 6, '211 - 911', 'pg/mL', 'Nerve conduction and red cell maturation.'),
            ],
            'Clinical Pathology & Urine': [
                ('URINE_RE', 'Urine Routine & Microscopic Examination', 'Urine', Decimal('150.00'), 1, 'Clear, Pale Yellow, Sugar: Nil, Albumin: Nil', '—', 'Kidney, urinary tract, and metabolic screening.'),
                ('URINE_CULTURE', 'Urine Culture & Sensitivity (Antibiotic Panel)', 'Urine', Decimal('650.00'), 24, 'No significant bacterial growth', 'CFU/mL', 'Identifies UTI organisms and antibiotic susceptibility.'),
                ('STOOL_RE', 'Stool Routine Examination', 'Stool', Decimal('150.00'), 2, 'Color: Brown, Occult Blood: Negative', '—', 'Digestive health and parasitic detection.'),
            ],
            'Serology & Infectious Fevers': [
                ('DENGUE_DUO', 'Dengue NS1 Antigen + IgM/IgG Antibodies', 'Blood', Decimal('850.00'), 2, 'Negative', '—', 'Early and secondary dengue fever diagnosis.'),
                ('WIDAL', 'Widal Slide Test (Typhoid Serology)', 'Blood', Decimal('220.00'), 2, 'S. typhi O/H: < 1:80', 'Titre', 'Enteric / Typhoid fever screening.'),
                ('CRP', 'C-Reactive Protein (Quantitative CRP)', 'Blood', Decimal('380.00'), 2, '< 6.0', 'mg/L', 'Acute systemic inflammation biomarker.'),
            ]
        }

        created_tests = []
        for cat_name, test_list in lab_data.items():
            cat_obj, _ = LabCategory.objects.get_or_create(
                name=cat_name,
                defaults={'description': f'Diagnostic investigations for {cat_name}'}
            )
            for t in test_list:
                test_obj, _ = LabTest.objects.get_or_create(
                    code=t[0],
                    defaults={
                        'category': cat_obj,
                        'name': t[1],
                        'sample_type': t[2],
                        'price': t[3],
                        'turnaround_hours': t[4],
                        'normal_range': t[5],
                        'unit': t[6],
                        'description': t[7],
                        'is_active': True,
                    }
                )
                created_tests.append(test_obj)

        # 4. Seed Patients
        patients_data = [
            {'first_name': 'Kaviarasan', 'last_name': 'M', 'phone': '9840111001', 'email': 'kavi@gmail.com', 'gender': 'male', 'blood': 'O+', 'dob': date(1988, 4, 12), 'address': '12, Razaak Garden, Aminjikarai, Chennai'},
            {'first_name': 'Deepika', 'last_name': 'Ramesh', 'phone': '9840111002', 'email': 'deepika.r@gmail.com', 'gender': 'female', 'blood': 'B+', 'dob': date(1994, 9, 21), 'address': '45/B, Ayyavoo Colony, Aminjikarai'},
            {'first_name': 'Subramanian', 'last_name': 'V', 'phone': '9840111003', 'email': 'subbu.v@yahoo.com', 'gender': 'male', 'blood': 'A+', 'dob': date(1965, 11, 5), 'address': '8, Vijayeswari St, Aminjikarai'},
            {'first_name': 'Pooja', 'last_name': 'Venkat', 'phone': '9840111004', 'email': 'pooja.v@outlook.com', 'gender': 'female', 'blood': 'AB+', 'dob': date(2001, 1, 18), 'address': '78, Poonamallee High Rd, Shenoy Nagar'},
            {'first_name': 'Mohammed', 'last_name': 'Irfan', 'phone': '9840111005', 'email': 'irfan.md@gmail.com', 'gender': 'male', 'blood': 'O-', 'dob': date(1982, 7, 30), 'address': '22, Mosque St, Aminjikarai'},
            {'first_name': 'Lakshmi', 'last_name': 'Narayanan', 'phone': '9840111006', 'email': 'lakshmi.n@gmail.com', 'gender': 'female', 'blood': 'B-', 'dob': date(1972, 3, 14), 'address': '104, Nelson Manickam Rd, Choolaimedu'},
            {'first_name': 'Vijay', 'last_name': 'Kumar', 'phone': '9840111007', 'email': 'vijay.k@gmail.com', 'gender': 'male', 'blood': 'A-', 'dob': date(1990, 8, 25), 'address': '19, 2nd Main Rd, Anna Nagar East'},
            {'first_name': 'Sowmya', 'last_name': 'Krishnan', 'phone': '9840111008', 'email': 'sowmya.k@gmail.com', 'gender': 'female', 'blood': 'O+', 'dob': date(1996, 12, 3), 'address': '33, Razaak Garden Main Rd, Aminjikarai'},
        ]

        created_patients = []
        for p in patients_data:
            pat_obj, _ = Patient.objects.get_or_create(
                phone=p['phone'],
                defaults={
                    'first_name': p['first_name'],
                    'last_name': p['last_name'],
                    'email': p['email'],
                    'gender': p['gender'],
                    'blood_group': p['blood'],
                    'date_of_birth': p['dob'],
                    'address': p['address'],
                    'medical_history': 'Essential Hypertension & Seasonal Allergies' if p['first_name'] in ['Subramanian', 'Lakshmi'] else 'None reported',
                }
            )
            created_patients.append(pat_obj)

        # 5. Generate Historical & Current Appointments, Prescriptions, Lab Orders, Invoices
        today = timezone.now().date()
        
        # Appointment time slots
        sample_times = [time(8, 30), time(9, 15), time(10, 0), time(11, 30), time(16, 30), time(17, 15), time(18, 0), time(19, 0)]
        
        statuses = ['completed', 'completed', 'completed', 'confirmed', 'scheduled', 'no_show', 'cancelled']

        for day_offset in range(-12, 3):
            target_date = today + timedelta(days=day_offset)
            
            for doc in created_doctors[:4]:
                # Pick 1-2 patients
                pat = random.choice(created_patients)
                appt_time = random.choice(sample_times)

                # Check double booking
                if not Appointment.objects.filter(doctor=doc, appointment_date=target_date, appointment_time=appt_time).exists():
                    current_status = 'completed' if day_offset < 0 else random.choice(['confirmed', 'scheduled'])
                    if day_offset < 0 and random.random() < 0.15:
                        current_status = 'no_show'
                    elif day_offset < 0 and random.random() < 0.1:
                        current_status = 'cancelled'

                    appt = Appointment.objects.create(
                        patient=pat,
                        doctor=doc,
                        appointment_date=target_date,
                        appointment_time=appt_time,
                        status=current_status,
                        fee=doc.consultation_fee,
                        reason='Routine clinical consultation & health checkup',
                    )

                    # If completed, create prescription and invoice
                    if current_status == 'completed':
                        rx = Prescription.objects.create(
                            appointment=appt,
                            diagnosis='Acute Upper Respiratory Tract Infection' if doc.specialization == 'General Physician' else 'Stage 1 Hypertension & Lipid Evaluation',
                            blood_pressure='126/82 mmHg',
                            pulse_rate='74 bpm',
                            temperature='98.6 F',
                            weight_kg=Decimal('68.5'),
                            advice_diet='Maintain low sodium diet, avoid oily foods, drink 3L warm water daily.',
                            follow_up_date=target_date + timedelta(days=14)
                        )
                        PrescriptionMedicine.objects.create(
                            prescription=rx,
                            medicine_name='Tab. Paracetamol 650mg',
                            dosage='1 Tab',
                            frequency='1-0-1 (Twice Daily After Food)',
                            duration_days=5,
                            instructions='Take after food'
                        )
                        PrescriptionMedicine.objects.create(
                            prescription=rx,
                            medicine_name='Tab. Pantocid 40mg',
                            dosage='1 Tab',
                            frequency='1-0-0 (Empty Stomach)',
                            duration_days=5,
                            instructions='Morning 30 mins before breakfast'
                        )

                        # Create paid invoice
                        method = random.choice(['upi', 'cash', 'card', 'upi'])
                        Invoice.objects.create(
                            patient=pat,
                            appointment=appt,
                            consultation_charges=doc.consultation_fee,
                            medicine_charges=Decimal('180.00'),
                            paid_amount=doc.consultation_fee + Decimal('180.00'),
                            payment_status='paid',
                            payment_method=method,
                            transaction_reference=f"UPI-{random.randint(100000000000, 999999999999)}" if method == 'upi' else ''
                        )

        # 6. Seed Lab Orders & Results
        for day_offset in range(-8, 1):
            order_date = today + timedelta(days=day_offset)
            pat = random.choice(created_patients)
            doc = random.choice(created_doctors)

            order = LabOrder.objects.create(
                patient=pat,
                doctor=doc,
                order_date=order_date,
                status='completed' if day_offset < 0 else 'sample_collected',
                priority=random.choice(['routine', 'routine', 'urgent']),
                sample_collected_at=timezone.now() - timedelta(days=abs(day_offset)),
                reported_at=timezone.now() - timedelta(days=abs(day_offset), hours=-2) if day_offset < 0 else None,
            )

            # Add 2-3 tests
            selected_tests = random.sample(created_tests, k=random.randint(2, 3))
            total = Decimal('0.00')
            for t in selected_tests:
                LabOrderItem.objects.create(
                    order=order,
                    test=t,
                    result_value='13.8' if t.code == 'HB' else ('95' if t.code == 'FBS' else 'Normal'),
                    reference_range=t.normal_range,
                    unit=t.unit,
                    is_abnormal=False
                )
                total += t.price

            order.total_amount = total
            order.save()

            if order.status == 'completed':
                Invoice.objects.create(
                    patient=pat,
                    lab_order=order,
                    lab_charges=total,
                    paid_amount=total,
                    payment_status='paid',
                    payment_method=random.choice(['upi', 'cash', 'card'])
                )

        self.stdout.write(self.style.SUCCESS('Successfully seeded Royal Care Clinic & Lab database with complete clinical & analytics records!'))
