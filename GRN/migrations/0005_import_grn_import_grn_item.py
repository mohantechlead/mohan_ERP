# Generated by Django 5.0.7 on 2024-08-05 11:46

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GRN', '0004_grn_item_description_grn_item_measurement_type_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='import_GRN',
            fields=[
                ('GRN_no', models.TextField(primary_key=True, serialize=False)),
                ('grn_date', models.DateField(blank=True, null=True)),
                ('recieved_from', models.TextField(blank=True, null=True)),
                ('transporter_name', models.TextField(blank=True, null=True)),
                ('truck_no', models.TextField(blank=True, null=True)),
                ('store_name', models.TextField(blank=True, null=True)),
                ('store_keeper', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='import_GRN_item',
            fields=[
                ('grn_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('item_name', models.TextField(blank=True, null=True)),
                ('quantity', models.FloatField()),
                ('measurement_type', models.TextField(blank=True, null=True)),
                ('remarks', models.TextField(blank=True, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('measurement_unit', models.TextField(blank=True, null=True)),
                ('no_of_bags', models.FloatField(blank=True, null=True)),
                ('per_unit_kg', models.FloatField(blank=True, null=True)),
                ('GRN_no', models.ForeignKey(db_column='GRN_no', on_delete=django.db.models.deletion.CASCADE, to='GRN.import_grn')),
            ],
        ),
    ]
