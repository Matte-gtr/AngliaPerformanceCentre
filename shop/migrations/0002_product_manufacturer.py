# Generated by Django 3.2.3 on 2022-04-08 15:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='manufacturer',
            field=models.CharField(default='mountune', max_length=255),
            preserve_default=False,
        ),
    ]
