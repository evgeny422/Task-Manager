from datetime import datetime
from django.shortcuts import redirect
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response

from .filters import IsOwnerFilterBackend
from .models import Task
from .permission import IsOwnerOrStaffOrReadOnly
from .serializers import *


class TaskListView(viewsets.ModelViewSet):
    queryset = Task.objects.filter(is_active=True)
    serializer_class = TaskListSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter, IsOwnerFilterBackend]
    filter_fields = ['category', 'user']  # ?user= ...
    search_fields = ['url', 'category']  # ?search= ...
    ordering_fields = ['started_at', 'created_at']  # ?ordering= ...
    permission_classes = [IsOwnerOrStaffOrReadOnly]


class TaskViewSet(viewsets.ViewSet):
    def retrieve(self, request, pk=None):
        queryset = Task.objects.get(pk=pk)
        serializer = TaskDetailSerializer(queryset)
        return Response(serializer.data)

    def delete(self, request, pk=None):
        queryset = Task.objects.get(pk=pk)
        queryset.is_active = False
        queryset.deleted_at = datetime.now()
        queryset.save()
        return redirect('task_list')


class AddTaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskCreateSerializer
