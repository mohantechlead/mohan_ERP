from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ("GRN", "0018_supplier_remarks_supplier_tin_no"),
    ]

    operations = [
        migrations.CreateModel(
            name="ActualPurchase",
            fields=[
                ("actual_purchase_id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("date", models.DateField(blank=True, null=True)),
                ("created_by", models.TextField(blank=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("pr_no", models.ForeignKey(db_column="pr_no", on_delete=django.db.models.deletion.CASCADE, to="GRN.purchase_orders")),
            ],
            options={
                "ordering": ["-created_at"],
            },
        ),
        migrations.CreateModel(
            name="ActualPurchaseItem",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("item_name", models.TextField(blank=True, null=True)),
                ("requested_quantity", models.FloatField(blank=True, null=True)),
                ("actual_quantity", models.FloatField(blank=True, null=True)),
                ("difference_quantity", models.FloatField(blank=True, null=True)),
                ("actual_purchase", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="items", to="GRN.actualpurchase")),
                ("pr_item", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to="GRN.pr_item")),
            ],
            options={
                "ordering": ["item_name"],
            },
        ),
    ]
