from django.urls import path
from . import views

urlpatterns = [
    path('', views.doctor_list, name='doctor_list'),
    path('create/', views.doctor_create, name='doctor_create'),
    path('<int:pk>/', views.doctor_detail, name='doctor_detail'),
    path('<int:pk>/edit/', views.doctor_edit, name='doctor_edit'),
]
