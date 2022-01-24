from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from . import views
from .views import method_get_create, method_get_update

urlpatterns = format_suffix_patterns([
    path("task/", views.TaskSetView.as_view({'get': 'list'}), name='task_list'),
    path("ur_task/", views.TaskSetView.as_view({'get': 'list_user'}), name='task_user_list'),
    path("task/<int:pk>/", views.TaskSetView.as_view({'get': 'retrieve'}), name='task_retrieve'),
    path("task/<int:pk>/finish", views.TaskSetView.as_view({'get': 'delete'}), name='task_finish'),
    path("task/create", views.TaskSetView.as_view({'post': 'create'}), name='task_create'),
    path('create_from_get/', method_get_create, name='create_task'),
    path("task/<int:pk>/update/", method_get_update, name='update_task'),
])

# urlpatterns += ...
