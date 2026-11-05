from django.http import JsonResponse, HttpResponse
from django.core.exceptions import PermissionDenied
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from apps.dashboard.decorators import role_required

from apps.projects.models import Project
from apps.tasks.models import Task

from .forms import TaskForm,TaskStatusForm
from .permissions import permission_task,can_delete_task

User = get_user_model()
@login_required
@role_required(User.Role.ADMIN,User.Role.MANAGER)
def task_create(request,project_pk):
    user = request.user
    projects = Project.objects.none()

    if user.role == User.Role.ADMIN:
        projects = Project.objects.all()
    elif user.role == User.Role.MANAGER:
        projects = Project.objects.filter(manager=user)

    project = get_object_or_404(projects,pk=project_pk)

    if request.method == 'POST':
        form = TaskForm(request.POST,user=user,project=project)

        form.instance.project = project

        if form.is_valid():
            task = form.save(commit=False)
            task.project = project
            task.save()

            response = HttpResponse(status=204)
            response['HX-Trigger'] = 'taskCreated'
            return response

    else:
        form = TaskForm(user=user,project=project)

    return render(request,'tasks/create.html',{'form':form,'project':project})
@login_required
def project_task_list(request,project_pk):
    user = request.user
    projects = Project.objects.none()

    if user.role == User.Role.ADMIN:
        projects = Project.objects.all()
    elif user.role == User.Role.MANAGER:
        projects = Project.objects.filter(
            Q(manager=user) | Q(members=user)
        ).distinct()
    else:
        projects = Project.objects.filter(
            members=user
        )
    project = get_object_or_404(projects,pk=project_pk)

    tasks = list(project.tasks.select_related('assigned_to','project'))
    tasks = permission_task(user,tasks)
    return render(request, 'tasks/_project_tasks.html', {'project':project,'tasks':tasks})

@login_required
def task_update(request,pk):
    user = request.user
    task = get_object_or_404(Task.objects.select_related('project','assigned_to'),pk=pk)

    if user.role == User.Role.ADMIN:
        form_class = TaskForm
        form = TaskForm(user=user,project=task.project,instance=task)

    elif user.role == User.Role.MANAGER and task.project.manager_id == user.pk:
        form_class = TaskForm
        form = TaskForm(user=user,project=task.project,instance=task)

    elif (
        user.role in (User.Role.MEMBER, User.Role.MANAGER)
        and task.project.members.filter(pk=user.pk).exists()
        and task.assigned_to_id == user.pk
    ) :
        form_class = TaskStatusForm
        form = TaskStatusForm(instance=task)
    else:
        raise PermissionDenied

    if request.method == 'POST':

        project = task.project

        if form_class == TaskForm:

            form = TaskForm(request.POST,user=user,project=project,instance=task)
        else:
            form = TaskStatusForm(request.POST,instance=task)

        if form.is_valid():

            form.save()

            response = HttpResponse(status=204)
            response['HX-Trigger'] = 'taskUpdated'
            return response

    return render(request,'tasks/update.html',{'form':form,'task':task})

@login_required
@require_POST
def task_delete(request,pk):
    user = request.user

    task = get_object_or_404(Task,pk=pk)

    if not can_delete_task(user,task):
        raise PermissionDenied

    task.delete()

    response = HttpResponse(status=204)
    response['HX-Trigger'] = 'taskDeleted'
    return response










