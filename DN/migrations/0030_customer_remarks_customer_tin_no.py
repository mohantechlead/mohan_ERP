# Generated by Django 5.0.7 on 2025-02-13 07:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DN', '0029_alter_inventory_order_items_group'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='remarks',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='customer',
            name='tin_no',
            field=models.CharField(blank=True, null=True),
        ),
    ]
