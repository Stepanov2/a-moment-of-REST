# Generated by Django 4.1.2 on 2022-11-10 15:31

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pereval', '0004_added_status_alter_added_add_time'),
    ]

    operations = [
        migrations.RenameField(
            model_name='added',
            old_name='altitude',
            new_name='height',
        ),
        migrations.AlterField(
            model_name='added',
            name='add_time',
            field=models.DateTimeField(default=datetime.datetime(2022, 11, 10, 15, 31, 39, 731455, tzinfo=datetime.timezone.utc)),
        ),
    ]
