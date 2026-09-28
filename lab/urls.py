from django.urls import path
from . import views

urlpatterns = [
    path('', views.lab_dashboard, name='lab_dashboard'),
    path('catalog/', views.test_catalog, name='test_catalog'),
    path('orders/', views.order_list, name='lab_order_list'),
    path('orders/create/', views.order_create, name='lab_order_create'),
    path('orders/<int:pk>/', views.order_detail, name='lab_order_detail'),
    path('orders/<int:pk>/status/<str:new_status>/', views.update_order_status, name='lab_order_status'),
    path('orders/<int:pk>/results/', views.enter_results, name='lab_enter_results'),
    path('orders/<int:pk>/print/', views.print_report, name='lab_report_print'),
]
