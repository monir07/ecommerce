# Generated by Django 4.1.1 on 2023-03-07 15:27

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('eshop', '0006_querymessage'),
    ]

    operations = [
        migrations.AddField(
            model_name='querymessage',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='querymessage',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
