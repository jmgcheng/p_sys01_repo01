from django.contrib import admin
from sales.models import SaleInvoiceCategory, SaleInvoiceStatus, SaleInvoiceHeader, SaleInvoiceDetail, OfficialReceiptStatus, OfficialReceiptHeader, OfficialReceiptDetail

admin.site.register(SaleInvoiceCategory)
admin.site.register(SaleInvoiceStatus)
admin.site.register(SaleInvoiceHeader)
admin.site.register(SaleInvoiceDetail)
admin.site.register(OfficialReceiptStatus)
admin.site.register(OfficialReceiptHeader)
admin.site.register(OfficialReceiptDetail)
