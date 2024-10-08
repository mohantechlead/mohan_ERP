# Generated by Django 5.0.7 on 2024-08-16 06:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('MR', '0013_mr_branch'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='inventory',
            options={'ordering': ['item_name']},
        ),
        migrations.AlterModelOptions(
            name='inventory_mr_items',
            options={'ordering': ['item_name']},
        ),
        migrations.AlterModelOptions(
            name='mr',
            options={'ordering': ['MR_no']},
        ),
        migrations.AlterModelOptions(
            name='mr_item',
            options={'ordering': ['MR_no']},
        ),
        migrations.AlterModelOptions(
            name='opening_balance',
            options={'ordering': ['item_name']},
        ),
    ]
