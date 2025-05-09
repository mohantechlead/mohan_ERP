
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DN', '0025_alter_delivery_options_alter_delivery_items_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='inventory_order_items',
            fields=[
                ('item_name', models.TextField(blank=True, primary_key=True, serialize=False)),
                ('total_no_of_unit', models.FloatField(blank=True, null=True)),
                ('total_quantity', models.FloatField(blank=True)),
                ('branch', models.TextField(blank=True, null=True)),
                ('group', models.TextField(blank=True, null=True)),
            ],
            options={
                'ordering': ['item_name'],
            },
        ),
    ]
