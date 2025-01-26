from django.urls import path
from analyses.views import AnalysisTableListView, ajx_employee_demographics, ajx_top_requested_items, ajx_sales_breakdown, ajx_top_selling_variations, ajx_monthly_sales_vs_purchases, ajx_receipts_payment_status, ajx_patient_purchases

app_name = 'analyses'

urlpatterns = [
    path('tables/', AnalysisTableListView.as_view(), name='analysis-table-list'),

    path('ajx_employee_demographics/', ajx_employee_demographics,
         name='ajx_employee_demographics'),
    path('ajx_top_requested_items/', ajx_top_requested_items,
         name='ajx_top_requested_items'),
    path('ajx_sales_breakdown/', ajx_sales_breakdown, name='ajx_sales_breakdown'),
    path('ajx_top_selling_variations/', ajx_top_selling_variations,
         name='ajx_top_selling_variations'),
    path('ajx_monthly_sales_vs_purchases/', ajx_monthly_sales_vs_purchases,
         name='ajx_monthly_sales_vs_purchases'),
    path('ajx_receipts_payment_status/', ajx_receipts_payment_status,
         name='ajx_receipts_payment_status'),
    path('ajx_patient_purchases/', ajx_patient_purchases,
         name='ajx_patient_purchases'),

    # path('', EmployeeListView.as_view(), name='employee-list'),
]
