# Generated by Django 4.1.2 on 2022-11-12 11:09

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pereval', '0005_rename_altitude_added_height_alter_added_add_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='added',
            name='add_time',
            field=models.DateTimeField(default=datetime.datetime(2022, 11, 12, 11, 9, 12, 581258, tzinfo=datetime.timezone.utc), null=True),
        ),
    ]
