from datetime import datetime

from django.shortcuts import redirect
from django.views.generic import ListView, DetailView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status

from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .exception_handling_func import base_view
from .logic import add_xml
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

    def finish(self, request, pk=None):
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

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)


@base_view
def method_get_create(request):
    """"Get-method создания задачи"""
    url = request.GET.get('url')
    category = request.GET.get('cat', 1)
    if (not url) or (url is None):
        raise Exception
    Task.objects.create(
        user=request.user,
        url=url,
        category=category,
        content=add_xml(url)
    )
    return redirect('tasks')


class TaskListView(ListView):
    """Список задач"""
    model = Task
    queryset = Task.objects.all()
    template_name = 'tasks/task_list.html'


class TaskDetailView(DetailView):
    """Задача по id"""
    model = Task
    template_name = 'tasks/task_detail.html'


class Search(ListView):
    """Поиск задачи по url"""
    template_name = 'tasks/task_list.html'

    def get_queryset(self):
        return Task.objects.filter(url__icontains=self.request.GET.get("q"))

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["q"] = self.request.GET.get("q")
        return context
