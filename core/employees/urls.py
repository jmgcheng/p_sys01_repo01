from django.urls import path
from employees.views import EmployeeListView, EmployeeCreateView, EmployeeDetailView, EmployeeUpdateView, ajx_employee_list, ajx_import_insert_excel_employees_celery, ajx_tasks_status


app_name = 'employees'

urlpatterns = [
    path('create/', EmployeeCreateView.as_view(), name='employee-create'),
    path('<int:pk>/', EmployeeDetailView.as_view(), name='employee-detail'),
    path('<int:pk>/update/', EmployeeUpdateView.as_view(), name='employee-update'),
    # path('<int:pk>/delete/', EmployeeDeleteView.as_view(), name='employee-delete'),

    path('ajx_employee_list/', ajx_employee_list, name='ajx_employee_list'),
    path('ajx_import_insert_excel_employees_celery', ajx_import_insert_excel_employees_celery,
         name='ajx_import_insert_excel_employees_celery'),
    path('ajx_tasks_status/<str:task_id>',
         ajx_tasks_status, name='ajx_tasks_status'),

    path('', EmployeeListView.as_view(), name='employee-list'),
]
