# Generated by Django 5.0.7 on 2024-11-26 07:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DN', '0026_inventory_order_items'),
    ]

    operations = [
        migrations.AddField(
            model_name='inventory_order_items',
            name='group',
            field=models.TextField(blank=True, null=True),
        ),
    ]
