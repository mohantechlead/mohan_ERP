# Generated by Django 5.0.7 on 2024-08-02 09:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('MR', '0007_inventory_branch'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='inventory',
            name='branch',
        ),
    ]
