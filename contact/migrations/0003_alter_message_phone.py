# Generated by Django 3.2.3 on 2021-12-15 13:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0002_rename_contact_message'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='phone',
            field=models.CharField(blank=True, max_length=20),
        ),
    ]
