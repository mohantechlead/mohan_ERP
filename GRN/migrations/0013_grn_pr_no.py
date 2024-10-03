# Generated by Django 5.0.7 on 2024-09-29 21:54

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("GRN", "0012_purchase_orders_vat"),
    ]

    operations = [
        migrations.AddField(
            model_name="grn",
            name="PR_no",
            field=models.ForeignKey(
                blank=True,
                db_column="PR_no",
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="GRN.purchase_orders",
            ),
        ),
    ]