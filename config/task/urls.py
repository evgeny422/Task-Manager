from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

urlpatterns = format_suffix_patterns([
    path("task/", views.TaskSetView.as_view({'get': 'list'}), name='task_list'),
    path("task/<int:pk>/", views.TaskSetView.as_view({'get': 'retrieve'}), name='task_retrieve'),
    path("task/<int:pk>/delete", views.TaskSetView.as_view({'get': 'delete'}), name='task_delete'),
    path("task/create", views.TaskSetView.as_view({'post': 'create'}), name='task_create'),

])
