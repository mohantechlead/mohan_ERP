# Generated by Django 5.0.7 on 2024-08-12 08:58

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MR', '0009_inventory_branch_mr_total_quantity'),
    ]

    operations = [
        migrations.CreateModel(
            name='opening_balance',
            fields=[
                ('item_name', models.TextField(blank=True)),
                ('no_of_unit', models.FloatField(blank=True, null=True)),
                ('unit_type', models.TextField(blank=True, null=True)),
                ('measurement_type', models.TextField(blank=True, null=True)),
                ('quantity', models.FloatField(blank=True)),
                ('balance_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('branch', models.TextField(blank=True, null=True)),
            ],
        ),
    ]
