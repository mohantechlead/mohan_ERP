# Generated by Django 5.0.7 on 2024-07-30 06:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('MR', '0004_mr_item_description_mr_item_measurement_unit_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='inventory',
            old_name='unit_measurment',
            new_name='measurement_type',
        ),
    ]