# Generated by Django 5.0.7 on 2024-10-07 01:46

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("GRN", "0013_grn_pr_no"),
    ]

    operations = [
        migrations.AlterField(
            model_name="purchase_orders",
            name="PR_no",
            field=models.TextField(
                db_column="pr_no", primary_key=True, serialize=False
            ),
        ),
    ]