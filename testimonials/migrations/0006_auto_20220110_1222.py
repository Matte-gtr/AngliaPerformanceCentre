# Generated by Django 3.2.3 on 2022-01-10 12:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testimonials', '0005_alter_reviewimages_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reviewimages',
            name='review',
        ),
        migrations.AddField(
            model_name='review',
            name='image',
            field=models.ManyToManyField(blank=True, to='testimonials.ReviewImages'),
        ),
    ]
