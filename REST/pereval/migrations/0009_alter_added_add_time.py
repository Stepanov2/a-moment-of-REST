# Generated by Django 4.1.2 on 2022-11-12 14:11

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('pereval', '0008_alter_added_add_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='added',
            name='add_time',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now),
        ),
    ]
