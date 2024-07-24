from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FGRN', '0003_fgrn_item_per_unit_kg'),
    ]

    operations = [
        migrations.CreateModel(
            name='finished_goods',
            fields=[
                ('item_name', models.TextField(primary_key=True, serialize=False)),
                ('quantity', models.FloatField()),
            ],
        ),
    ]

