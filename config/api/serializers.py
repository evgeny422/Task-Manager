from django.contrib.auth.models import User
from rest_framework import serializers

from task.models import Task
from task.logic import add_xml

import sys

sys.path.append(".")


class UserDetailSerializer(serializers.ModelSerializer):
    """"Описание пользователя"""

    class Meta:
        model = User
        fields = ("id", "username", "first_name", "last_name", "email")


class TaskListSerializer(serializers.ModelSerializer):
    """Вывод всех задач"""

    user = UserDetailSerializer(read_only=True)

    class Meta:
        model = Task
        fields = ("id", "url", "status", "user", "category", "is_active", "response", 'started_at', 'created_at')


class TaskDetailSerializer(serializers.ModelSerializer):
    """ Описание задачи """

    class Meta:
        model = Task
        fields = '__all__'


class TaskCreateSerializer(serializers.ModelSerializer):
    """Добавление задач пользователем"""

    class Meta:
        model = Task
        fields = ("url", "category", "user")

    def create(self, validated_data):
        task = Task.objects.create(
            url=validated_data.get('url', None),
            category=validated_data.get('category', None),
            user=validated_data.get('user', ),
            content=add_xml(validated_data.get('url', None)),
        )
        task.save()
        return task
