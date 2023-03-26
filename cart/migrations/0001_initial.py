# Generated by Django 4.1.1 on 2023-03-25 16:49

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=25)),
                ('discount', models.PositiveIntegerField(help_text='Discount in percentage')),
                ('active', models.BooleanField(default=True)),
                ('active_date', models.DateField()),
                ('expiry_date', models.DateField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]