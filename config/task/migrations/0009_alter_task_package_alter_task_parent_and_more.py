# Generated by Django 4.0.1 on 2022-02-16 06:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('task', '0008_task_package_task_parent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='package',
            field=models.IntegerField(default=None, null=True, verbose_name='PackageID'),
        ),
        migrations.AlterField(
            model_name='task',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='task.task', verbose_name='Задача'),
        ),
        migrations.AlterField(
            model_name='task',
            name='status',
            field=models.PositiveSmallIntegerField(choices=[(1, ' Успешно'), (2, 'Ошибка'), (3, 'Действие 3')], null=True, verbose_name='Оценка'),
        ),
        migrations.AlterField(
            model_name='task',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
    ]
