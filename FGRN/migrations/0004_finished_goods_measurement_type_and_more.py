# Generated by Django 5.0.7 on 2024-08-01 07:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FGRN', '0003_fgrn_item_per_unit_kg'),
    ]

    operations = [
        migrations.AddField(
            model_name='finished_goods',
            name='measurement_type',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='finished_goods',
            name='no_of_unit',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='finished_goods',
            name='unit_type',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='finished_goods',
            name='quantity',
            field=models.FloatField(blank=True, null=True),
        ),
    ]