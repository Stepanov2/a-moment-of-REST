# Generated by Django 4.1.2 on 2022-11-12 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pereval', '0009_alter_added_add_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='added',
            name='add_time',
            field=models.DateTimeField(),
        ),
    ]
