# Generated by Django 5.0.7 on 2024-09-06 06:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('DN', '0012_delivery_items_serial_no_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='delivery_items',
            name='serial_no',
        ),
    ]
