from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from patients.models import Patient
from doctors.models import Doctor
from appointments.models import Appointment
from lab.models import LabTest, LabOrder
from billing.models import Invoice
from reports.analytics import ClinicAnalyticsEngine
from .serializers import (
    PatientSerializer, DoctorSerializer, AppointmentSerializer,
    LabTestSerializer, LabOrderSerializer, InvoiceSerializer
)

class PatientListCreateView(generics.ListCreateAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [permissions.IsAuthenticated]

class PatientDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [permissions.IsAuthenticated]

class DoctorListView(generics.ListAPIView):
    queryset = Doctor.objects.filter(is_available=True).select_related('user')
    serializer_class = DoctorSerializer
    permission_classes = [permissions.AllowAny]

class AppointmentListCreateView(generics.ListCreateAPIView):
    queryset = Appointment.objects.select_related('patient', 'doctor__user').all()
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = super().get_queryset()
        status_param = self.request.query_params.get('status')
        date_param = self.request.query_params.get('date')
        if status_param:
            qs = qs.filter(status=status_param)
        if date_param:
            qs = qs.filter(appointment_date=date_param)
        return qs

class AppointmentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated]

class LabTestListView(generics.ListAPIView):
    queryset = LabTest.objects.filter(is_active=True).select_related('category')
    serializer_class = LabTestSerializer
    permission_classes = [permissions.AllowAny]

class LabOrderListCreateView(generics.ListCreateAPIView):
    queryset = LabOrder.objects.select_related('patient', 'doctor__user').prefetch_related('items__test').all()
    serializer_class = LabOrderSerializer
    permission_classes = [permissions.IsAuthenticated]

class InvoiceListCreateView(generics.ListCreateAPIView):
    queryset = Invoice.objects.select_related('patient').all()
    serializer_class = InvoiceSerializer
    permission_classes = [permissions.IsAuthenticated]

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def api_analytics_summary(request):
    summary = ClinicAnalyticsEngine.get_summary_metrics()
    return Response(summary)
