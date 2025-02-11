from django.db import models


class VendorCategory(models.Model):
    name = models.CharField(max_length=50, unique=True)
    # RETAIL, DISTRIBUTOR, WHOLESALER

    def __str__(self):
        return self.name


class Vendor(models.Model):
    name = models.CharField(max_length=200, blank=True)
    category = models.ForeignKey(
        VendorCategory, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name
