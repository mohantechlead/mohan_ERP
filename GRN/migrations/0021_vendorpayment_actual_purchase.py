import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("GRN", "0020_vendorpayment"),
    ]

    operations = [
        migrations.AddField(
            model_name="vendorpayment",
            name="actual_purchase",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="linked_payments",
                to="GRN.actualpurchase",
            ),
        ),
    ]
