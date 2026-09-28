from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.analytics_dashboard, name='analytics_dashboard'),
    path('export/excel/', views.export_excel_report, name='export_excel_report'),
    path('export/csv/<str:dataset_name>/', views.export_csv_report, name='export_csv_report'),
    path('export/powerbi/', views.export_powerbi_bundle, name='export_powerbi_bundle'),
]
