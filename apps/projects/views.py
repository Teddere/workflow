from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q #combiner plusieurs conditions avec l'opérateur
from django.contrib import messages

from django.contrib.auth import get_user_model
from apps.dashboard.decorators import role_required

from django.core.paginator import Paginator
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

    query = request.GET.get('q','').strip()
    status = request.GET.get('status','').strip()

    if query:
        projects = projects.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )
    if status in Project.Status.values:
        projects = projects.filter(status=status)

    projects_list = (
        projects
        .select_related('manager')
        .prefetch_related('members')
        .order_by('-created_at', '-pk')
    )

    paginator = Paginator(projects_list, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
            'projects': page_obj,
            'query':query,
            'status':status,
        }

    return render(request,'project/list.html',context)

@login_required
def project_detail(request):
    return render(request,'project/detail.html')





