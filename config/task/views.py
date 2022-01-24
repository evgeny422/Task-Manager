from datetime import datetime

from django.shortcuts import redirect
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Task

from .serializers import *


class TaskSetView(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskListSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter, ]
    filter_fields = ['category', 'user']  # ?user= ...
    search_fields = ['url', 'category']  # ?search= ...
    ordering_fields = ['started_at', 'created_at']  # ?ordering= ...
    #permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        queryset = Task.objects.filter(is_active=True)
        filtered_queryset = self.filter_queryset(queryset)
        serializer = TaskListSerializer(filtered_queryset, many=True)
        return Response(serializer.data)

    def list_user(self, request, *args, **kwargs):
        queryset = Task.objects.filter(is_active=True, user=request.user.id)
        filtered_queryset = self.filter_queryset(queryset)
        serializer = TaskListSerializer(filtered_queryset, many=True)
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
        return redirect('task_list')

    def create(self, request, *args, **kwargs):
        serializer = TaskCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    #   return redirect('task_list')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
