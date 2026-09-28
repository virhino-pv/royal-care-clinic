from django.urls import path
from . import views

urlpatterns = [
    path('', views.appointment_list, name='appointment_list'),
    path('create/', views.appointment_create, name='appointment_create'),
    path('<int:pk>/', views.appointment_detail, name='appointment_detail'),
    path('<int:pk>/edit/', views.appointment_edit, name='appointment_edit'),
    path('<int:pk>/status/<str:new_status>/', views.appointment_status_update, name='appointment_status_update'),
    path('slots/<int:doctor_id>/', views.get_doctor_slots_api, name='doctor_slots_api'),
]
