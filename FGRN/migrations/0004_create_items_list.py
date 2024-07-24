migrations.CreateModel(
            name='finished_goods',
            fields=[
                ('item_name', models.TextField(primary_key=True, serialize=False)),
                ('quantity', models.FloatField()),
            ],
        ),
