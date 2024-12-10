from django.contrib import admin
from products.models import ProductUnit, ProductSize, ProductColor, Product, ProductVariation

admin.site.register(ProductUnit)
admin.site.register(ProductSize)
admin.site.register(ProductColor)
admin.site.register(Product)
admin.site.register(ProductVariation)
