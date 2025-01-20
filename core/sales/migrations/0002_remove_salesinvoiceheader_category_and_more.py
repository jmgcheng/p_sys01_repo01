# Generated by Django 5.1.3 on 2025-01-20 08:20

import datetime
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0001_initial'),
        ('employees', '0004_alter_employee_company_id_alter_employee_contact'),
        ('products', '0002_alter_productsize_name_alter_productunit_name'),
        ('sales', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='salesinvoiceheader',
            name='category',
        ),
        migrations.RemoveField(
            model_name='salesinvoiceheader',
            name='creator',
        ),
        migrations.RemoveField(
            model_name='salesinvoiceheader',
            name='customer',
        ),
        migrations.RemoveField(
            model_name='salesinvoiceheader',
            name='status',
        ),
        migrations.RenameModel(
            old_name='SalesInvoiceStatus',
            new_name='SaleInvoiceCategory',
        ),
        migrations.RenameModel(
            old_name='SalesInvoiceCategory',
            new_name='SaleInvoiceStatus',
        ),
        migrations.CreateModel(
            name='SaleInvoiceHeader',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=50, unique=True)),
                ('date', models.DateField(default=datetime.datetime.now)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sales.saleinvoicecategory')),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sale_invoice_creator', to='employees.employee')),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='customers.customer')),
                ('status', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sales.saleinvoicestatus')),
            ],
        ),
        migrations.CreateModel(
            name='SaleInvoiceDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity_request', models.PositiveIntegerField(default=0)),
                ('product_variation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sale_invoice_product_variation', to='products.productvariation')),
                ('sales_invoice_header', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='sales.saleinvoiceheader')),
            ],
        ),
        migrations.DeleteModel(
            name='SalesInvoiceDetail',
        ),
        migrations.DeleteModel(
            name='SalesInvoiceHeader',
        ),
    ]
