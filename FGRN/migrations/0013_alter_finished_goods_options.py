# Generated by Django 5.0.7 on 2024-10-01 18:55

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("FGRN", "0012_alter_fgrn_item_item_name"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="finished_goods",
            options={"ordering": ["item_name"]},
        ),
    ]
