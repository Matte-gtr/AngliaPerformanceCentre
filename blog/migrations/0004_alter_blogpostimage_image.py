# Generated by Django 3.2.3 on 2022-02-13 22:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20220213_2209'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpostimage',
            name='image',
            field=models.FileField(upload_to='blogs'),
        ),
    ]
