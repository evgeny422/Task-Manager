from django.utils import timezone
from django.http import Http404
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView

from .XML_validation import xml_valid

from .exception_handling_func import base_view
from .logic import add_xml, content_check_xml
from .models import Task


@base_view
def method_get_create(request):
    """"Get-method создания задачи"""
    url = request.GET.get('url')
    category = request.GET.get('cat', 1)
    content = add_xml(url)
    if not xml_valid(content):
        raise Exception('XML FILE NOT VALID')

    if (not url) or (url is None):
        raise Exception('HAVE NOT URL')

    Task.objects.create(
        user=request.user,
        url=url,
        category=category,
        content=content,
    )
    return redirect('tasks')


@base_view
def create_package(request, pk=None):
    try:
        child_task = Task.objects.get(pk=pk)
    except Task.DoesNotExist:
        raise Http404("Task does not exist")

    if child_task.package:
        Task.objects.create(
            user=request.user,
            url=child_task.url,
            category=child_task.category,
            package=child_task.package,
            content=content_check_xml(child_task.package),
            parent=child_task,
            created_at=timezone.now()
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

    @base_view
    def get_queryset(self):
        return Task.objects.filter(url__icontains=self.request.GET.get("q").strip())

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["q"] = self.request.GET.get("q")
        return context
