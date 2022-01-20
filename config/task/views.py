from datetime import datetime

from django.shortcuts import redirect
from django_filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions, viewsets
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from .logic import add_XML

from .models import Task
from .serializers import *
from django.utils import timezone


class TaskViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = Task.objects.filter(is_active=True)
        serializer = TaskListSerializer(queryset, many=True)
        filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter,)
        filter_fields = ('category',)  # ?category = ...
        search_fields = ['url', 'category', ]  # ?search= ...
        ordering_fields = ['started_at', 'created_at']

        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Task.objects.get(pk=pk)
        serializer = TaskDetailSerializer(queryset)
        return Response(serializer.data)

    def delete(self, request, pk=None):
        queryset = Task.objects.get(pk=pk)
        queryset.is_active = False
        queryset.deleted_at = datetime.now()
        queryset.save()
        return redirect('task-list')


class AddTaskViewSet(viewsets.ModelViewSet):
    """Добавление рейтинга фильму"""
    serializer_class = TaskCreateSerializer


