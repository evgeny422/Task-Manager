# Generated by Django 4.0.1 on 2022-01-19 12:34

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0003_alter_task_updated_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 1, 19, 12, 34, 7, 564046, tzinfo=utc), editable=False),
        ),
    ]
