# Generated by Django 5.0.7 on 2024-07-26 09:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MR', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='inventory',
            name='no_of_unit',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='inventory',
            name='unit_measurment',
            field=models.TextField(blank=True, null=True),
        ),
    ]