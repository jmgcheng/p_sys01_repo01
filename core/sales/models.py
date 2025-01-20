from datetime import datetime
from django.db import models
from products.models import ProductVariation
from employees.models import Employee
from customers.models import Customer


class SaleInvoiceCategory(models.Model):
    name = models.CharField(max_length=50, unique=True, null=False)
    # RETAIL, PATIENT, WHOLESALE, GOVERNMENT, CORPORATE

    def save(self, *args, **kwargs):
        self.name = self.name.upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class SaleInvoiceStatus(models.Model):
    name = models.CharField(max_length=50, unique=True, null=False)

    def save(self, *args, **kwargs):
        self.name = self.name.upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class SaleInvoiceHeader(models.Model):
    code = models.CharField(max_length=50, unique=True,
                            blank=False, null=False)
    date = models.DateField(default=datetime.now)
    category = models.ForeignKey(
        SaleInvoiceCategory, on_delete=models.CASCADE)
    creator = models.ForeignKey(
        Employee, on_delete=models.CASCADE, related_name="sale_invoice_creator")
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, blank=True, null=True)
    status = models.ForeignKey(SaleInvoiceStatus, on_delete=models.CASCADE)

    def __str__(self):
        return f"SaleInvoiceHeader #{self.code}"


class SaleInvoiceDetail(models.Model):
    sale_invoice_header = models.ForeignKey(
        SaleInvoiceHeader, on_delete=models.CASCADE, blank=False, null=True)
    product_variation = models.ForeignKey(
        ProductVariation, on_delete=models.CASCADE, related_name="sale_invoice_product_variation")
    quantity_request = models.PositiveIntegerField(
        default=0, blank=False, null=False)

    def __str__(self):
        return f"SaleInvoiceDetail #{self.id}"


class OfficialReceiptStatus(models.Model):
    name = models.CharField(max_length=50, unique=True, null=False)
    # PAID, UNPAID, VOID, CANCELLED

    def save(self, *args, **kwargs):
        self.name = self.name.upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class OfficialReceiptHeader(models.Model):
    code = models.CharField(max_length=50, unique=True,
                            blank=False, null=False)
    date = models.DateField(default=datetime.now)
    status = models.ForeignKey(OfficialReceiptStatus, on_delete=models.CASCADE)
    creator = models.ForeignKey(
        Employee, on_delete=models.CASCADE, related_name="official_receipt_creator")
    sale_invoice_header = models.ForeignKey(
        SaleInvoiceHeader, on_delete=models.CASCADE, blank=False, null=True, default=1)

    def __str__(self):
        return f"OfficialReceiptHeader #{self.code}"


class OfficialReceiptDetail(models.Model):
    official_receipt_header = models.ForeignKey(
        OfficialReceiptHeader, on_delete=models.CASCADE, blank=False, null=True)
    product_variation = models.ForeignKey(
        ProductVariation, on_delete=models.CASCADE, related_name="official_receipt_product_variation")
    quantity_paid = models.PositiveIntegerField(
        default=0, blank=False, null=False)

    def __str__(self):
        return f"OfficialReceiptDetail #{self.id}"
