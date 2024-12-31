from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('DN', '0026_inventory_order_items'),
    ]

   operations = [
        migrations.AlterField(
            model_name="delivery",
            name="phone_number",
            field=models.CharField(max_length=15),
        ),
    ]

