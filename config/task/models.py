from django.contrib.auth.models import User
from django.db import models
from .logic import add_xml

from django.utils import timezone


# https://nextcloud.tspu.edu.ru/index.php/s/baFfs2scWk6SikG

class Task(models.Model):
    """" Задачи для пользователя """

    CATEGORY_CHOICES = (
        (1, 'Действие 1'),
        (2, 'Действие 2'),
        (3, 'Действие 3'),
        (4, 'Действие 4'),
        (5, 'Действие 5'),
    )

    STATUS_CHOICES = (
        (1, ' Успешно'),
        (2, 'Ошибка'),
        (3, 'Ожидание'),
    )

    url = models.CharField('url', max_length=150)
    content = models.TextField(blank=True)
    response = models.TextField(default=None, null=True)
    status = models.PositiveSmallIntegerField('Ответ', choices=STATUS_CHOICES, null=True)
    is_active = models.BooleanField(default=True)
    category = models.PositiveSmallIntegerField('Тип задачи', choices=CATEGORY_CHOICES, null=True)
    started_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(default=None, null=True, blank=True)
    created_at = models.DateTimeField(editable=False)
    updated_at = models.DateTimeField(editable=False)
    deleted_at = models.DateTimeField(default=None, null=True, blank=True)
    user = models.ForeignKey(User, verbose_name="Пользователь", on_delete=models.SET_NULL, null=True)
    package = models.IntegerField("PackageID", default=None, null=True)
    parent = models.ForeignKey(
        'self', verbose_name="Задача", on_delete=models.SET_NULL, blank=True, null=True
    )

    def __str__(self):
        return f'URL: {self.pk} {self.url}- {self.category}-Status: {self.status}'

    def save(self, *args, **kwargs):
        """" Обновление поля self.updated_at при обновлении контента + XML """
        if (not self.id) and (not self.package):
            self.created_at = timezone.now()
            self.content = add_xml(self.url)

        self.updated_at = timezone.now()
        return super(Task, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Задача"
        verbose_name_plural = "Задачи"

