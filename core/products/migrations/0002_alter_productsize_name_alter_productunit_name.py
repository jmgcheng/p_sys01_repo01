# Generated by Django 5.1.3 on 2024-12-10 03:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productsize',
            name='name',
            field=models.CharField(max_length=20, unique=True),
        ),
        migrations.AlterField(
            model_name='productunit',
            name='name',
            field=models.CharField(max_length=20, unique=True),
        ),
    ]