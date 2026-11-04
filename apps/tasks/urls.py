from django.urls import path

from . import views


app_name = 'tasks'

urlpatterns = [
    path('<int:project_pk>/tasks/new/',views.task_create,name='create'),
    path('<int:project_pk>/tasks/list/',views.project_task_list,name='project-task-list')
]