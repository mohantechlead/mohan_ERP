# Generated by Django 5.0.7 on 2024-08-13 11:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MR', '0012_remove_inventory_mr_items_measurement_type_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='mr',
            name='branch',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
