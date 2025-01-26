from django.urls import path
from analyses.views import AnalysisTableListView

app_name = 'analyses'

urlpatterns = [
    path('tables/', AnalysisTableListView.as_view(), name='analysis-table-list'),

    # path('ajx_employee_list/', ajx_employee_list, name='ajx_employee_list'),

    # path('', EmployeeListView.as_view(), name='employee-list'),
]
