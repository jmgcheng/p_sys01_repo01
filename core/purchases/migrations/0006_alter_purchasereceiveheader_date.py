# Generated by Django 5.1.3 on 2025-01-20 02:55

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('purchases', '0005_rename_quantity_receive_purchasereceivedetail_quantity_received'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchasereceiveheader',
            name='date',
            field=models.DateField(default=datetime.datetime.now),
        ),
    ]
