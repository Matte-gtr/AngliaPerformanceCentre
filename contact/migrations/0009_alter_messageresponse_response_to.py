# Generated by Django 3.2.3 on 2022-01-24 12:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0008_messageresponse_message_header'),
    ]

    operations = [
        migrations.AlterField(
            model_name='messageresponse',
            name='response_to',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='responses', to='contact.message'),
        ),
    ]
