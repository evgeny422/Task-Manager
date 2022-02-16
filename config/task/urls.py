from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from .views import method_get_create, TaskListView, TaskDetailView, Search, create_package

urlpatterns = format_suffix_patterns([
    # path("task/", views.TaskSetView.as_view({'get': 'list'}), name='task_list'),
    # path("ur_task/", views.TaskSetView.as_view({'get': 'list_user'}), name='task_user_list'),
    # path("task/<int:pk>/", views.TaskSetView.as_view({'get': 'retrieve'}), name='task_retrieve'),
    # path("task/<int:pk>/finish", views.TaskSetView.as_view({'get': 'finish'}), name='task_finish'),
    # path("task/create", views.TaskSetView.as_view({'post': 'create'}), name='task_create'),
    # path('create_from_get/', method_get_create, name='create_task'),
    # path("task/<int:pk>/update/", views.TaskSetView.as_view({'patch': 'update'}), name='update'),

    path('create_from_get/', method_get_create, name='create_task'),
    path("search/", Search.as_view(), name="search"),
    path('list/', TaskListView.as_view(), name='tasks'),
    path('list/<int:pk>/', TaskDetailView.as_view(), name='task_id'),
    path('list/<int:pk>/add_to_queue', create_package, name='add_to_queue'),


])
