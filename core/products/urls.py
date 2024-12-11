from django.urls import path
from products.views import ProductVariationListView, ajx_product_variation_list

app_name = 'products'

urlpatterns = [
    # path('create/', EmployeeCreateView.as_view(), name='employee-create'),
    # path('variations/create/', ProductVariationCreateView.as_view(), name='product-variation-create'),


    # path('<int:pk>/', EmployeeDetailView.as_view(), name='employee-detail'),
    # path('<int:pk>/update/', EmployeeUpdateView.as_view(), name='employee-update'),
    # # path('<int:pk>/delete/', EmployeeDeleteView.as_view(), name='employee-delete'),

    # path('ajx_employee_list/', ajx_employee_list, name='ajx_employee_list'),
    path('variations/ajx_product_variation_list/',
         ajx_product_variation_list, name='ajx_product_variation_list'),
    # path('ajx_export_excel_all_employees/', ajx_export_excel_all_employees,
    #      name='ajx_export_excel_all_employees'),
    # path('ajx_export_excel_filtered_employees/', ajx_export_excel_filtered_employees,
    #      name='ajx_export_excel_filtered_employees'),
    # path('ajx_import_insert_excel_employees_celery', ajx_import_insert_excel_employees_celery,
    #      name='ajx_import_insert_excel_employees_celery'),
    # path('ajx_import_update_excel_employees_celery', ajx_import_update_excel_employees_celery,
    #      name='ajx_import_update_excel_employees_celery'),
    # path('ajx_tasks_status/<str:task_id>',
    #      ajx_tasks_status, name='ajx_tasks_status'),

    # path('', EmployeeListView.as_view(), name='employee-list'),
    path('variations/', ProductVariationListView.as_view(),
         name='product-variation-list'),
]