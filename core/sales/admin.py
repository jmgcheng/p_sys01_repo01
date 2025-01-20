from django.contrib import admin
from sales.models import SaleInvoiceCategory, SaleInvoiceStatus, SaleInvoiceHeader, SaleInvoiceDetail

admin.site.register(SaleInvoiceCategory)
admin.site.register(SaleInvoiceStatus)
admin.site.register(SaleInvoiceHeader)
admin.site.register(SaleInvoiceDetail)
