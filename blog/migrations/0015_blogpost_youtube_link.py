# Generated by Django 3.2.3 on 2022-03-17 12:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0014_alter_blogpostvideo_video'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpost',
            name='youtube_link',
            field=models.CharField(blank=True, max_length=500),
        ),
    ]
