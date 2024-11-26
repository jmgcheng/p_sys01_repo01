from django.urls import path
from employees.views import EmployeeListView
# , EmployeeDetailView, EmployeeCreateView, EmployeeUpdateView,

app_name = 'employees'

urlpatterns = [
    # path('create/', EmployeeCreateView.as_view(), name='employee-create'),
    # path('<int:pk>/', EmployeeDetailView.as_view(), name='employee-detail'),
    # path('<int:pk>/update/', EmployeeUpdateView.as_view(), name='employee-update'),
    # path('<int:pk>/delete/', EmployeeDeleteView.as_view(), name='employee-delete'),

    path('', EmployeeListView.as_view(), name='employee-list'),
]
