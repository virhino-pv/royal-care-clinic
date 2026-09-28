from django.urls import path
from . import views

urlpatterns = [
    path('', views.prescription_list, name='prescription_list'),
    path('create/<int:appointment_id>/', views.prescription_create, name='prescription_create'),
    path('<int:pk>/', views.prescription_detail, name='prescription_detail'),
    path('<int:pk>/print/', views.prescription_print, name='prescription_print'),
]
