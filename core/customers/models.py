from django.db import models


class CustomerCategory(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Customer(models.Model):
    customer_id = models.CharField(max_length=50, unique=True, default='')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True)
    category = models.ForeignKey(
        CustomerCategory, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
