# Generated by Django 5.0.7 on 2024-09-23 12:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GRN', '0010_rename_name_supplier_contact_person'),
    ]

    operations = [
        migrations.AddField(
            model_name='supplier',
            name='address',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
    ]