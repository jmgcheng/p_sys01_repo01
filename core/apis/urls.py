from django.urls import path
from products.views import ProductListCreateViewApi, ProductRetrieveUpdateDestroyViewApi, ProductVariationListCreateViewApi, ProductVariationRetrieveUpdateDestroyViewApi
from employees.views import EmployeeListCreateViewApi, EmployeeRetrieveUpdateDestroyViewApi
from purchases.views import PurchaseRequestListCreateViewApi, PurchaseRequestRetrieveUpdateDestroyViewApi, PurchaseReceiveListCreateViewApi, PurchaseReceiveRetrieveUpdateDestroyViewApi
from sales.views import SaleInvoiceListCreateViewApi, SaleInvoiceRetrieveUpdateDestroyViewApi, OfficialReceiptListCreateViewApi, OfficialReceiptRetrieveUpdateDestroyViewApi
from inventories.views import InventoryListViewAPI
from apis.views import GetCustomAuthToken
from rest_framework.authtoken import views

app_name = 'api'

urlpatterns = [

    path('products/', ProductListCreateViewApi.as_view()),
    path('products/<int:pk>/', ProductRetrieveUpdateDestroyViewApi.as_view()),

    path('products/variations/', ProductVariationListCreateViewApi.as_view()),
    path('products/variations/<int:pk>/',
         ProductVariationRetrieveUpdateDestroyViewApi.as_view()),

    path('employees/', EmployeeListCreateViewApi.as_view()),
    path('employees/<int:pk>/', EmployeeRetrieveUpdateDestroyViewApi.as_view()),

    path('purchase-requests/', PurchaseRequestListCreateViewApi.as_view()),
    path('purchase-requests/<int:pk>/',
         PurchaseRequestRetrieveUpdateDestroyViewApi.as_view()),

    path('purchase-receives/', PurchaseReceiveListCreateViewApi.as_view()),
    path('purchase-receives/<int:pk>/',
         PurchaseReceiveRetrieveUpdateDestroyViewApi.as_view()),

    path('sale-invoices/', SaleInvoiceListCreateViewApi.as_view()),
    path('sale-invoices/<int:pk>/',
         SaleInvoiceRetrieveUpdateDestroyViewApi.as_view()),

    path('official-receipts/', OfficialReceiptListCreateViewApi.as_view()),
    path('official-receipts/<int:pk>/',
         OfficialReceiptRetrieveUpdateDestroyViewApi.as_view()),

    path('inventory-summary/', InventoryListViewAPI.as_view()),

    # use this one if you don't want a customize response
    # path('login/', views.obtain_auth_token),
    path('login/', GetCustomAuthToken.as_view()),

]
