# Generated by Django 3.2.3 on 2022-02-15 21:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_auto_20220215_2134'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpost',
            name='public',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='blogpost',
            name='post_body',
            field=models.TextField(blank=True),
        ),
    ]
