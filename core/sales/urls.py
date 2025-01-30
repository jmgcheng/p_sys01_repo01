from django.urls import path
from sales.views import SaleInvoiceCreateView, SaleInvoiceUpdateView, SaleInvoiceListView, SaleInvoiceDetailView, SaleInvoiceDetailPdfView, OfficialReceiptCreateView, OfficialReceiptUpdateView, OfficialReceiptListView, OfficialReceiptDetailView, ajx_sale_invoice_list, ajx_official_receipt_list

app_name = 'sales'

urlpatterns = [

    path('invoices/create/', SaleInvoiceCreateView.as_view(),
         name='sale-invoice-create'),

    path('receipts/create/', OfficialReceiptCreateView.as_view(),
         name='official-receipt-create'),

    path('invoices/<int:pk>/update/', SaleInvoiceUpdateView.as_view(),
         name='sale-invoice-update'),

    path('receipts/<int:pk>/update/', OfficialReceiptUpdateView.as_view(),
         name='official-receipt-update'),

    path('invoices/<int:pk>/', SaleInvoiceDetailView.as_view(),
         name='sale-invoice-detail'),


    path('invoices/<int:pk>/pdf', SaleInvoiceDetailPdfView,
         name='sale-invoice-detail-pdf'),

    path('receipts/<int:pk>/', OfficialReceiptDetailView.as_view(),
         name='official-receipt-detail'),

    path('invoices/', SaleInvoiceListView.as_view(),
         name='sale-invoice-list'),

    path('receipts/', OfficialReceiptListView.as_view(),
         name='official-receipt-list'),

    path('invoices/ajx_sale_invoice_list/',
         ajx_sale_invoice_list, name='ajx_sale_invoice_list'),

    path('receipts/ajx_official_receipt_list/',
         ajx_official_receipt_list, name='ajx_official_receipt_list'),

]
