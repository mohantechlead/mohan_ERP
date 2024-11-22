# Generated by Django 5.0.7 on 2024-11-21 06:05

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DN', '0025_alter_delivery_options_alter_delivery_items_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='inventory_order_items',
            fields=[
                ('item_name', models.TextField(blank=True)),
                ('total_no_of_unit', models.FloatField(blank=True, null=True)),
                ('total_quantity', models.FloatField(blank=True)),
                ('balance_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('branch', models.TextField(blank=True, null=True)),
            ],
            options={
                'ordering': ['item_name'],
            },
        ),
    ]
