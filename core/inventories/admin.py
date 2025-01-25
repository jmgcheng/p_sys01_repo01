from django.contrib import admin
from inventories.models import InventoryAddHeader, InventoryAddDetail, InventoryDeductHeader, InventoryDeductDetail

admin.site.register(InventoryAddHeader)
admin.site.register(InventoryAddDetail)
admin.site.register(InventoryDeductHeader)
admin.site.register(InventoryDeductDetail)
