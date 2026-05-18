import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='WIP',
            fields=[
                ('WIP_no', models.TextField(primary_key=True, serialize=False)),
                ('date', models.DateField()),
                ('work_center', models.TextField(blank=True, null=True)),
                ('notes', models.TextField(blank=True, null=True)),
                ('branch', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'ordering': ['WIP_no'],
            },
        ),
        migrations.CreateModel(
            name='WIP_item',
            fields=[
                ('item_id', models.AutoField(primary_key=True, serialize=False)),
                ('item_name', models.TextField()),
                ('quantity', models.FloatField(blank=True, null=True)),
                ('no_of_unit', models.FloatField(blank=True, null=True)),
                ('unit_type', models.TextField(blank=True, null=True)),
                ('remarks', models.TextField(blank=True, null=True)),
                (
                    'WIP_no',
                    models.ForeignKey(
                        db_column='WIP_no',
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='wip_items',
                        to='wip.wip',
                    ),
                ),
            ],
            options={
                'ordering': ['WIP_no', 'item_id'],
            },
        ),
    ]
