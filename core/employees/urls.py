from django.urls import path
from employees.views import EmployeeListView, EmployeeCreateView, ajx_employee_list
# , EmployeeDetailView, EmployeeUpdateView,

app_name = 'employees'

urlpatterns = [
    path('create/', EmployeeCreateView.as_view(), name='employee-create'),
    # path('<int:pk>/', EmployeeDetailView.as_view(), name='employee-detail'),
    # path('<int:pk>/update/', EmployeeUpdateView.as_view(), name='employee-update'),
    # path('<int:pk>/delete/', EmployeeDeleteView.as_view(), name='employee-delete'),

    path('ajx_employee_list/', ajx_employee_list, name='ajx_employee_list'),

    path('', EmployeeListView.as_view(), name='employee-list'),
]
