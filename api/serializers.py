from rest_framework import serializers
from accounts.models import User
from patients.models import Patient
from doctors.models import Doctor
from appointments.models import Appointment
from lab.models import LabCategory, LabTest, LabOrder, LabOrderItem
from prescriptions.models import Prescription, PrescriptionMedicine
from billing.models import Invoice

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'role', 'phone']

class PatientSerializer(serializers.ModelSerializer):
    full_name = serializers.ReadOnlyField()
    age = serializers.ReadOnlyField()

    class Meta:
        model = Patient
        fields = [
            'id', 'first_name', 'last_name', 'full_name', 'phone', 'email',
            'date_of_birth', 'age', 'gender', 'blood_group', 'address',
            'emergency_contact', 'allergies', 'medical_history', 'created_at'
        ]

class DoctorSerializer(serializers.ModelSerializer):
    doctor_name = serializers.ReadOnlyField()
    email = serializers.EmailField(source='user.email', read_only=True)
    phone = serializers.CharField(source='user.phone', read_only=True)

    class Meta:
        model = Doctor
        fields = [
            'id', 'doctor_name', 'specialization', 'qualification',
            'experience_years', 'consultation_fee', 'room_number',
            'available_days', 'start_time', 'end_time', 'is_available', 'email', 'phone'
        ]

class AppointmentSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient.full_name', read_only=True)
    doctor_name = serializers.CharField(source='doctor.doctor_name', read_only=True)

    class Meta:
        model = Appointment
        fields = [
            'id', 'patient', 'patient_name', 'doctor', 'doctor_name',
            'appointment_date', 'appointment_time', 'appointment_type',
            'status', 'fee', 'reason', 'doctor_notes', 'created_at'
        ]

class LabTestSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = LabTest
        fields = [
            'id', 'code', 'name', 'category', 'category_name',
            'sample_type', 'price', 'turnaround_hours', 'normal_range', 'unit', 'description'
        ]

class LabOrderItemSerializer(serializers.ModelSerializer):
    test_name = serializers.CharField(source='test.name', read_only=True)
    test_code = serializers.CharField(source='test.code', read_only=True)

    class Meta:
        model = LabOrderItem
        fields = [
            'id', 'test', 'test_name', 'test_code',
            'result_value', 'reference_range', 'unit', 'is_abnormal', 'technician_remarks'
        ]

class LabOrderSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient.full_name', read_only=True)
    doctor_name = serializers.CharField(source='doctor.doctor_name', read_only=True)
    items = LabOrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = LabOrder
        fields = [
            'id', 'order_number', 'patient', 'patient_name', 'doctor', 'doctor_name',
            'order_date', 'status', 'priority', 'total_amount', 'sample_collected_at',
            'reported_at', 'notes', 'items', 'created_at'
        ]

class PrescriptionMedicineSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrescriptionMedicine
        fields = ['id', 'medicine_name', 'dosage', 'frequency', 'duration_days', 'instructions']

class PrescriptionSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='appointment.patient.full_name', read_only=True)
    doctor_name = serializers.CharField(source='appointment.doctor.doctor_name', read_only=True)
    medicines = PrescriptionMedicineSerializer(many=True, read_only=True)

    class Meta:
        model = Prescription
        fields = [
            'id', 'appointment', 'patient_name', 'doctor_name',
            'diagnosis', 'chief_complaints', 'blood_pressure', 'pulse_rate',
            'temperature', 'weight_kg', 'advice_diet', 'follow_up_date', 'medicines', 'created_at'
        ]

class InvoiceSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient.full_name', read_only=True)
    balance_due = serializers.ReadOnlyField()

    class Meta:
        model = Invoice
        fields = [
            'id', 'invoice_number', 'patient', 'patient_name', 'appointment', 'lab_order',
            'consultation_charges', 'lab_charges', 'medicine_charges', 'other_charges',
            'discount_amount', 'tax_amount', 'total_amount', 'paid_amount', 'balance_due',
            'payment_status', 'payment_method', 'transaction_reference', 'created_at'
        ]
