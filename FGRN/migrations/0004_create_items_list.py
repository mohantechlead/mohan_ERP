from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FGRN', '0003_fgrn_item_per_unit_kg'),
    ]

    operations = [
        migrations.CreateModel(
             name='items_list',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('item_name', models.TextField()),
            ],
        ),
    ]

