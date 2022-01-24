from datetime import datetime

from django.shortcuts import redirect
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status

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

    # permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        """"Вывод всех задач без привязки к юзеру"""
        queryset = Task.objects.filter(is_active=True)
        filtered_queryset = self.filter_queryset(queryset)
        serializer = TaskListSerializer(filtered_queryset, many=True)
        return Response(serializer.data)

    def list_user(self, request, *args, **kwargs):
        """"Вывод всех задач с привязкой к юзеру"""
        queryset = Task.objects.filter(is_active=True, user=request.user.id)
        filtered_queryset = self.filter_queryset(queryset)
        serializer = TaskListSerializer(filtered_queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """"Вывод задачи по id"""
        queryset = Task.objects.get(pk=pk)
        serializer = TaskDetailSerializer(queryset)
        return Response(serializer.data)

    def delete(self, request, pk=None):
        """"Soft-delete по id"""
        queryset = Task.objects.get(pk=pk)
        queryset.is_active = False
        queryset.deleted_at = datetime.now()
        queryset.save()
        return redirect('task_list')

    def create(self, request, *args, **kwargs):
        """"Post-method создания задачи"""
        serializer = TaskCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    #   return redirect('task_list')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


def method_get_create(request):
    """"Get-method создания задачи"""
    url, category = request.GET.get('url', None), request.GET.get('cat', 1)
    Task.objects.create(user=request.user, url=url, category=category, content=add_XML(url))
    return redirect('task_list')


def method_get_update(request, pk=None):
    """"Update-get-method"""
    default_task = Task.objects.get(id=pk)
    url = request.GET.get('url', default_task.url)
    category = request.GET.get('cat', default_task.category)
    Task.objects.filter(id=pk).update(url=url, category=category, content=add_XML(url),
                                      created_at=default_task.created_at, updated_at=timezone.now())
    return redirect('task_list')
