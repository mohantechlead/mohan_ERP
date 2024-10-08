# Generated by Django 5.0.7 on 2024-10-07 02:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("GRN", "0016_purchase_orders_excise_tax"),
    ]

    operations = [
        migrations.AlterField(
            model_name="pr_item",
            name="PR_no",
            field=models.ForeignKey(
                blank=True,
                db_column="pr_no",
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="GRN.purchase_orders",
            ),
        ),
    ]
