# Generated by Django 4.0.1 on 2022-01-27 06:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0006_alter_task_content_alter_task_response'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='response',
            field=models.TextField(default=None, null=True),
        ),
    ]
