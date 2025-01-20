from datetime import datetime
from django.db import models
from products.models import ProductVariation
from employees.models import Employee


class InventoryAddHeader(models.Model):
    code = models.CharField(max_length=50, unique=True,
                            blank=False, null=False, default=0)
    date = models.DateField(default=datetime.now)
    adder = models.ForeignKey(Employee, on_delete=models.CASCADE, default=0)

    def __str__(self):
        return f"InventoryAddHeader #{self.code}"


class InventoryAddDetail(models.Model):
    inventory_add_header = models.ForeignKey(
        InventoryAddHeader, on_delete=models.CASCADE, blank=False, null=True)
    product_variation = models.ForeignKey(
        ProductVariation, on_delete=models.CASCADE, related_name="inventory_add_product_variation", default=0)
    quantity_added = models.PositiveIntegerField(
        default=0, blank=False, null=False)

    def __str__(self):
        return f"InventoryAddDetail #{self.id}"
