from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wip', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='wip_item',
            name='measurement_type',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='wip_item',
            name='per_unit_kg',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
