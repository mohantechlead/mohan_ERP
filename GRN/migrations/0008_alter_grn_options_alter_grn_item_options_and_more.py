# Generated by Django 5.0.7 on 2024-08-16 06:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('GRN', '0007_inventory_grn_items'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='grn',
            options={'ordering': ['GRN_no']},
        ),
        migrations.AlterModelOptions(
            name='grn_item',
            options={'ordering': ['GRN_no']},
        ),
        migrations.AlterModelOptions(
            name='hs_code',
            options={'ordering': ['item_name']},
        ),
        migrations.AlterModelOptions(
            name='import_grn',
            options={'ordering': ['GRN_no']},
        ),
        migrations.AlterModelOptions(
            name='import_grn_item',
            options={'ordering': ['GRN_no']},
        ),
        migrations.AlterModelOptions(
            name='inventory_grn_items',
            options={'ordering': ['item_name']},
        ),
        migrations.RenameField(
            model_name='grn',
            old_name='grn_date',
            new_name='date',
        ),
        migrations.RenameField(
            model_name='import_grn',
            old_name='grn_date',
            new_name='date',
        ),
    ]
