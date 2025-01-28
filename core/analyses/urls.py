from django.urls import path
from analyses.views import AnalysisTableListView, AnalysisChartListView, ajx_employee_demographics_age, ajx_top_products, ajx_sales_breakdown_category, ajx_chart_employee_demographics_age, ajx_chart_top_products, ajx_chart_sales_breakdown_category

app_name = 'analyses'

urlpatterns = [
    path('tables/', AnalysisTableListView.as_view(), name='analysis-table-list'),

    path('charts/', AnalysisChartListView.as_view(), name='analysis-chart-list'),

    path('ajx_employee_demographics_age/', ajx_employee_demographics_age,
         name='ajx_employee_demographics_age'),
    path('ajx_top_products/', ajx_top_products,
         name='ajx_top_products'),
    path('ajx_sales_breakdown_category/', ajx_sales_breakdown_category,
         name='ajx_sales_breakdown_category'),

    # path('ajx_top_selling_variations/', ajx_top_selling_variations,
    #      name='ajx_top_selling_variations'),
    # path('ajx_monthly_sales_vs_purchases/', ajx_monthly_sales_vs_purchases,
    #      name='ajx_monthly_sales_vs_purchases'),
    # path('ajx_receipts_payment_status/', ajx_receipts_payment_status,
    #      name='ajx_receipts_payment_status'),
    # path('ajx_patient_purchases/', ajx_patient_purchases,
    #      name='ajx_patient_purchases'),


    path('ajx_chart_employee_demographics_age/', ajx_chart_employee_demographics_age,
         name='ajx_chart_employee_demographics_age'),
    path('ajx_chart_top_products/', ajx_chart_top_products,
         name='ajx_chart_top_products'),
    path('ajx_chart_sales_breakdown_category/', ajx_chart_sales_breakdown_category,
         name='ajx_chart_sales_breakdown_category'),

    # path('', EmployeeListView.as_view(), name='employee-list'),
]
