# Generated by Django 5.0.7 on 2024-09-23 11:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('GRN', '0009_supplier'),
    ]

    operations = [
        migrations.RenameField(
            model_name='supplier',
            old_name='name',
            new_name='contact_person',
        ),
    ]
