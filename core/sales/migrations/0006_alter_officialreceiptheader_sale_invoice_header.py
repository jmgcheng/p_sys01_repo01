# Generated by Django 5.1.3 on 2025-01-20 10:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0005_officialreceiptheader_sale_invoice_header'),
    ]

    operations = [
        migrations.AlterField(
            model_name='officialreceiptheader',
            name='sale_invoice_header',
            field=models.ForeignKey(default=1, null=True, on_delete=django.db.models.deletion.CASCADE, to='sales.saleinvoiceheader'),
        ),
    ]
