from django.http import JsonResponse, HttpResponse
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.contrib.auth.decorators import login_required

from apps.dashboard.decorators import role_required

from apps.projects.models import Project
from apps.tasks.models import Task
from .forms import TaskForm,TaskStatusForm

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
    return render(request, 'tasks/_project_tasks.html', {'project':project})

def task_update(request,pk):
    user = request.user
    task = Task.objects.get(pk=pk)

    if user.role == User.Role.ADMIN:
        form = TaskForm()
    elif user.role == User.Role.MANAGER and user == task.project.manager:
        form = TaskForm()

    elif user == task.project.members:
        form = TaskStatusForm()



