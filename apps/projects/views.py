from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q #combiner plusieurs conditions avec l'opérateur
from django.contrib import messages

from django.contrib.auth import get_user_model
from apps.dashboard.decorators import role_required
from .forms import ProjectForm
from .models import Project

User = get_user_model()
@login_required
@role_required(User.Role.ADMIN,User.Role.MANAGER)
def project_create(request):

    if request.method == 'POST':
        form = ProjectForm(request.POST,user=request.user)

        if form.is_valid():
            project = form.save()
            messages.success(request, f'Projet {project.title} a été créé avec succès!')
            return redirect('dashboard:home')
    else:
        # Les membres sélectionnés sont conservés.
        form = ProjectForm(user=request.user)
    selected_members = [
        str(pk) for pk in form['members'].value() or []
    ]


    context = {
        'form': form,
        'users': form.fields['members'].queryset,
        'selected_members': selected_members,
    }

    return render(request,'project/create.html',context)
@login_required
def project_list(request):
    user = request.user

    if user.role == User.Role.ADMIN:
        projects = Project.objects.all()

    elif user.role == User.Role.MANAGER:
        projects = Project.objects.filter(
            Q(manager=user) | Q(members=user)
        ).distinct()   #éviter les doublons

    else:
        projects = Project.objects.filter(
            Q(members=user)
        ).distinct()

    projects_list = projects.select_related('manager').prefetch_related('members')

    context = {
            'projects': projects_list.order_by('-created_at')
        }

    return render(request,'project/list.html',context)




