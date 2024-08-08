# Generated by Django 5.0.7 on 2024-08-02 13:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FGRN', '0007_fgrn_item_unit_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='fgrn',
            name='total_Pkg',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='fgrn',
            name='total_bags',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='fgrn',
            name='total_crt',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
