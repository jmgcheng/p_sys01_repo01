from django.db import models
from django.db.models import Sum
from django.conf import settings
from django.utils.text import slugify
from django.urls import reverse
from html_sanitizer.django import get_sanitizer


class ProductUnit(models.Model):
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name


class ProductSize(models.Model):
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name


class ProductColor(models.Model):
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    code = models.CharField(max_length=30, unique=True,
                            blank=False, null=False)
    name = models.CharField(max_length=50, unique=True,
                            blank=False, null=False)
    excerpt = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    image_url = models.CharField(max_length=2083, blank=True, null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        sanitizer = get_sanitizer()
        self.excerpt = sanitizer.sanitize(self.excerpt)
        self.description = sanitizer.sanitize(self.description)

        super().save(*args, **kwargs)


class ProductVariation(models.Model):
    code = models.CharField(max_length=30, unique=True,
                            blank=False, null=False)
    product = models.ForeignKey(
        Product, on_delete=models.SET_NULL, blank=False, null=True, related_name="product")
    name = models.CharField(max_length=50, unique=True,
                            blank=False, null=False)
    excerpt = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    unit = models.ForeignKey(ProductUnit, on_delete=models.SET_NULL,
                             blank=False, null=True, related_name="product_unit")
    size = models.ForeignKey(ProductSize, on_delete=models.SET_NULL,
                             blank=True, null=True, related_name="product_size")
    color = models.ForeignKey(ProductColor, on_delete=models.SET_NULL,
                              blank=True, null=True, related_name="product_color")
    image_url = models.CharField(max_length=2083, blank=True, null=True)
    quantity_alert = models.IntegerField(default=100)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        sanitizer = get_sanitizer()
        self.excerpt = sanitizer.sanitize(self.excerpt)
        self.description = sanitizer.sanitize(self.description)

        super().save(*args, **kwargs)

    def quantity_manual_add(self):
        return getattr(self, "quantity_manual_add_annotated", 0)

    def quantity_manual_deduct(self):
        return getattr(self, "quantity_manual_deduct_annotated", 0)

    def quantity_purchasing(self):
        return getattr(self, "quantity_purchasing_annotated", 0)

    def quantity_purchasing_receive(self):
        return getattr(self, "quantity_purchasing_receive_annotated", 0)

    def quantity_sale_releasing(self):
        return getattr(self, "quantity_sale_releasing_annotated", 0)

    def quantity_sold(self):
        return getattr(self, "quantity_sold_annotated", 0)

    def quantity_on_hand(self):
        return getattr(self, "quantity_on_hand_annotated", 0)
