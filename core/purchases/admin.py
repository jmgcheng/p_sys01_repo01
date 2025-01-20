from django.contrib import admin
from products.models import ProductUnit, ProductSize, ProductColor, Product, ProductVariation
from purchases.models import PurchaseRequestStatus, PurchaseRequestHeader, PurchaseRequestDetail, PurchaseReceiveHeader, PurchaseReceiveDetail

admin.site.register(PurchaseRequestStatus)
admin.site.register(PurchaseRequestHeader)
admin.site.register(PurchaseRequestDetail)
admin.site.register(PurchaseReceiveHeader)
admin.site.register(PurchaseReceiveDetail)
