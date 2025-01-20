# Generated by Django 5.1.3 on 2025-01-20 02:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0004_alter_employee_company_id_alter_employee_contact'),
        ('products', '0002_alter_productsize_name_alter_productunit_name'),
        ('purchases', '0003_purchaserequestheader_approver_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchasereceivedetail',
            name='product_variation',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='purchase_receive_product_variation', to='products.productvariation'),
        ),
        migrations.AddField(
            model_name='purchasereceivedetail',
            name='purchase_receive_header',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='purchases.purchasereceiveheader'),
        ),
        migrations.AddField(
            model_name='purchasereceivedetail',
            name='quantity_receive',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='purchasereceiveheader',
            name='code',
            field=models.CharField(default=0, max_length=50, unique=True),
        ),
        migrations.AddField(
            model_name='purchasereceiveheader',
            name='date',
            field=models.DateField(auto_now=True),
        ),
        migrations.AddField(
            model_name='purchasereceiveheader',
            name='purchase_request_header',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='purchases.purchaserequestheader'),
        ),
        migrations.AddField(
            model_name='purchasereceiveheader',
            name='receiver',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='employees.employee'),
        ),
    ]
