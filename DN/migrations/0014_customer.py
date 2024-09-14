# Generated by Django 5.0.7 on 2024-09-14 01:47

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("DN", "0013_remove_delivery_items_serial_no"),
    ]

    operations = [
        migrations.CreateModel(
            name="Customer",
            fields=[
                (
                    "customer_id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                ("phone_number", models.CharField(max_length=15)),
                ("email", models.EmailField(max_length=254, unique=True)),
                ("company", models.CharField(max_length=100)),
            ],
        ),
    ]