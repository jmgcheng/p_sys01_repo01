# Generated by Django 5.1.3 on 2025-01-20 10:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('purchases', '0006_alter_purchasereceiveheader_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='PurchaseReceiveStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
            ],
        ),
    ]
