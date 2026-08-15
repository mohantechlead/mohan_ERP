from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("DN", "0030_customer_remarks_customer_tin_no"),
    ]

    operations = [
        migrations.AddField(
            model_name="orders",
            name="is_void",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="orders",
            name="status",
            field=models.TextField(blank=True, default="active", null=True),
        ),
        migrations.AddField(
            model_name="orders",
            name="void_requested",
            field=models.BooleanField(default=False),
        ),
    ]
