# Generated by Django 5.0.7 on 2024-07-24 05:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FGRN', '0002_fgrn_total_quantity'),
    ]

    operations = [
        migrations.AddField(
            model_name='fgrn_item',
            name='per_unit_kg',
            field=models.FloatField(blank=True, null=True),
        ),
    ]