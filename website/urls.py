from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('services/', views.medical_services, name='services'),
    path('lab-services/', views.lab_services, name='lab_services'),
    path('doctors/', views.doctor_profiles, name='doctors'),
    path('timings/', views.timings, name='timings'),
    path('gallery/', views.gallery, name='gallery'),
    path('faq/', views.faq, name='faq'),
    path('contact/', views.contact, name='contact'),
    path('book-appointment/', views.book_appointment, name='book_appointment'),
    path('book-lab-test/', views.book_lab_test, name='book_lab_test'),
]
