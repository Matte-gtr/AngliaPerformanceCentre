# Generated by Django 3.2.3 on 2022-01-24 12:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0007_alter_messageresponse_response_to'),
    ]

    operations = [
        migrations.AddField(
            model_name='messageresponse',
            name='message_header',
            field=models.CharField(default='Reply', max_length=100),
            preserve_default=False,
        ),
    ]
