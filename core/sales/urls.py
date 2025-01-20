from django.urls import path
from sales.views import SaleInvoiceCreateView, SaleInvoiceUpdateView, SaleInvoiceListView, SaleInvoiceDetailView, ajx_sale_invoice_list

app_name = 'sales'

urlpatterns = [

    path('invoices/create/', SaleInvoiceCreateView.as_view(),
         name='sale-invoice-create'),

    path('invoices/<int:pk>/update/', SaleInvoiceUpdateView.as_view(),
         name='sale-invoice-update'),

    path('invoices/<int:pk>/', SaleInvoiceDetailView.as_view(),
         name='sale-invoice-detail'),

    path('invoices/', SaleInvoiceListView.as_view(),
         name='sale-invoice-list'),

    path('invoices/ajx_sale_invoice_list/',
         ajx_sale_invoice_list, name='ajx_sale_invoice_list'),

]
