# Generated by Django 5.0.7 on 2024-09-28 17:11

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("GRN", "0011_supplier_address"),
    ]

    operations = [
        migrations.AddField(
            model_name="purchase_orders",
            name="vat",
            field=models.FloatField(blank=True, null=True),
        ),
    ]
