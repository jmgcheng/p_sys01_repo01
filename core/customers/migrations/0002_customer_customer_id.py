# Generated by Django 5.1.3 on 2025-01-31 16:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='customer_id',
            field=models.CharField(default='', max_length=50, unique=True),
        ),
    ]
