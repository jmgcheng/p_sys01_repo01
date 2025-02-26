from django.urls import path
from products.views import ProductListCreateViewApi, ProductRetrieveUpdateDestroyViewApi, ProductVariationListCreateViewApi, ProductVariationRetrieveUpdateDestroyViewApi
from employees.views import EmployeeListCreateViewApi, EmployeeRetrieveUpdateDestroyViewApi

app_name = 'api'

urlpatterns = [

    path('products/', ProductListCreateViewApi.as_view()),
    path('products/<int:pk>/', ProductRetrieveUpdateDestroyViewApi.as_view()),

    path('products/variations/', ProductVariationListCreateViewApi.as_view()),
    path('products/variations/<int:pk>/',
         ProductVariationRetrieveUpdateDestroyViewApi.as_view()),

    path('employees/', EmployeeListCreateViewApi.as_view()),
    path('employees/<int:pk>/', EmployeeRetrieveUpdateDestroyViewApi.as_view()),

]
