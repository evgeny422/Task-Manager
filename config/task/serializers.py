from rest_framework import serializers

from .models import *


class TaskListSerializer(serializers.ModelSerializer):
    """Вывод всех задач"""

    class Meta:
        model = Task
        fields = ("url", "user", "category", 'started_at', 'created_at')


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
        )
        task.save()
        return task
