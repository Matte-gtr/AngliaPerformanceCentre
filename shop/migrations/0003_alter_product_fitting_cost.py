# Generated by Django 3.2.3 on 2022-05-06 10:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_product_manufacturer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='fitting_cost',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True),
        ),
    ]
