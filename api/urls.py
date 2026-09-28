from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from . import views

urlpatterns = [
    # JWT Authentication Endpoints
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Patient Endpoints
    path('patients/', views.PatientListCreateView.as_view(), name='api_patient_list'),
    path('patients/<int:pk>/', views.PatientDetailView.as_view(), name='api_patient_detail'),

    # Doctor Endpoints
    path('doctors/', views.DoctorListView.as_view(), name='api_doctor_list'),

    # Appointment Endpoints
    path('appointments/', views.AppointmentListCreateView.as_view(), name='api_appointment_list'),
    path('appointments/<int:pk>/', views.AppointmentDetailView.as_view(), name='api_appointment_detail'),

    # Diagnostic Lab Endpoints
    path('lab/tests/', views.LabTestListView.as_view(), name='api_lab_test_list'),
    path('lab/orders/', views.LabOrderListCreateView.as_view(), name='api_lab_order_list'),

    # Billing Endpoints
    path('billing/invoices/', views.InvoiceListCreateView.as_view(), name='api_invoice_list'),

    # Analytics Endpoint
    path('analytics/summary/', views.api_analytics_summary, name='api_analytics_summary'),
]
