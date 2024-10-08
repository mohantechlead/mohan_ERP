# Generated by Django 5.0.7 on 2024-08-12 11:44

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MR', '0010_opening_balance'),
    ]

    operations = [
        migrations.CreateModel(
            name='inventory_MR_items',
            fields=[
                ('item_name', models.TextField(blank=True)),
                ('total_no_of_unit', models.FloatField(blank=True, null=True)),
                ('unit_type', models.TextField(blank=True, null=True)),
                ('measurement_type', models.TextField(blank=True, null=True)),
                ('total_quantity', models.FloatField(blank=True)),
                ('balance_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('branch', models.TextField(blank=True, null=True)),
            ],
        ),
    ]
