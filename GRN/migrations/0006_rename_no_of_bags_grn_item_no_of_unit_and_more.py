# Generated by Django 5.0.7 on 2024-08-05 12:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('GRN', '0005_import_grn_import_grn_item'),
    ]

    operations = [
        migrations.RenameField(
            model_name='grn_item',
            old_name='no_of_bags',
            new_name='no_of_unit',
        ),
        migrations.RenameField(
            model_name='import_grn_item',
            old_name='no_of_bags',
            new_name='no_of_unit',
        ),
    ]
