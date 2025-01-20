from datetime import datetime
from django.db import models
from products.models import ProductVariation
from employees.models import Employee
from vendors.models import Vendor


class PurchaseRequestStatus(models.Model):
    name = models.CharField(max_length=50, unique=True, null=False)
    # OPEN (FOR APPROVAL), OPEN (PURCHASING), CLOSED, CANCELLED, REJECTED

    def save(self, *args, **kwargs):
        self.name = self.name.upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class PurchaseRequestHeader(models.Model):
    code = models.CharField(max_length=50, unique=True,
                            blank=False, null=False)
    date = models.DateField()
    requestor = models.ForeignKey(
        Employee, on_delete=models.CASCADE, related_name="purchase_request_requestor")
    approver = models.ForeignKey(
        Employee, on_delete=models.CASCADE, related_name="purchase_request_approver", blank=True, null=True)
    vendor = models.ForeignKey(
        Vendor, on_delete=models.CASCADE, blank=True, null=True)
    status = models.ForeignKey(PurchaseRequestStatus, on_delete=models.CASCADE)

    def __str__(self):
        return f"PurchaseRequestHeader #{self.code}"


class PurchaseRequestDetail(models.Model):
    purchase_request_header = models.ForeignKey(
        PurchaseRequestHeader, on_delete=models.CASCADE, blank=False, null=True)
    product_variation = models.ForeignKey(
        ProductVariation, on_delete=models.CASCADE, related_name="purchase_request_product_variation")
    quantity_request = models.PositiveIntegerField(
        default=0, blank=False, null=False)

    def __str__(self):
        return f"PurchaseRequestDetail #{self.id}"


class PurchaseReceiveStatus(models.Model):
    name = models.CharField(max_length=50, unique=True, null=False)
    # RECEIVED (NO ISSUE), RECEIVED (WITH ISSUE), CLOSED, CANCELLED

    def save(self, *args, **kwargs):
        self.name = self.name.upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class PurchaseReceiveHeader(models.Model):
    code = models.CharField(max_length=50, unique=True,
                            blank=False, null=False, default=0)
    date = models.DateField(default=datetime.now)
    receiver = models.ForeignKey(Employee, on_delete=models.CASCADE, default=0)
    purchase_request_header = models.ForeignKey(
        PurchaseRequestHeader, on_delete=models.CASCADE, blank=False, null=True)
    status = models.ForeignKey(
        PurchaseReceiveStatus, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return f"PurchaseReceiveHeader #{self.code}"


class PurchaseReceiveDetail(models.Model):
    purchase_receive_header = models.ForeignKey(
        PurchaseReceiveHeader, on_delete=models.CASCADE, blank=False, null=True)
    product_variation = models.ForeignKey(
        ProductVariation, on_delete=models.CASCADE, related_name="purchase_receive_product_variation", default=0)
    quantity_received = models.PositiveIntegerField(
        default=0, blank=False, null=False)

    def __str__(self):
        return f"PurchaseReceiveDetail #{self.id}"
