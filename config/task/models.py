from django.contrib.auth.models import User
from django.db import models
import datetime

from django.utils import timezone
from safedelete import SOFT_DELETE
from safedelete.models import SafeDeleteModel


class Task(models.Model):
    """" Задачи для пользователя """

    RATE_CHOICES = (
        (1, 'Действие 1'),
        (2, 'Действие 2'),
        (3, 'Действие 3'),
        (4, 'Действие 4'),
        (5, 'Действие 5'),
    )

    url = models.CharField('url', max_length=150)
    content = models.TextField()
    response = models.TextField()
    status = models.BooleanField('Выполнено', default=False)
    is_active = models.BooleanField(default=True)
    category = models.PositiveSmallIntegerField('Тип задачи', choices=RATE_CHOICES, null=True)
    started_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(default=None, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(editable=False, default=timezone.now())
    deleted_at = models.DateTimeField(default=None, null=True,blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'URL: {self.url}- {self.category}-Status: {self.status}'



    def save(self, *args, **kwargs):
        """"Обновление поля self.updated_at при обновлении контента"""
        if not self.id:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        return super(Task, self).save(*args, **kwargs)