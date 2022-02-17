from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from .views import method_get_create, TaskListView, TaskDetailView, Search, create_package

urlpatterns = format_suffix_patterns([

    path('create_from_get/', method_get_create, name='create_task'),
    path("search/", Search.as_view(), name="search"),
    path('list/', TaskListView.as_view(), name='tasks'),
    path('list/<int:pk>/', TaskDetailView.as_view(), name='task_id'),
    path('list/<int:pk>/add_to_queue', create_package, name='add_to_queue'),

])
