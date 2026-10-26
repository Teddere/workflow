from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

from .decorators import role_required


User = get_user_model()
@login_required
@role_required(User.Role.ADMIN,User.Role.MANAGER,User.Role.MEMBER)
def home(request):

    user = request.user

    if user.role == User.Role.ADMIN:
        pageTitle = 'Administrateur'

    elif user.role == User.Role.MANAGER:
        pageTitle = 'Manager'
    else:
        pageTitle ='Membre'
    context = {
        'pageTitle':f'Bienvenue sur TerWorkflow {pageTitle}',
        'role': user.role,
        'totalProjects':12,
        'totalTasks':48,
        'tasksCompleted':32,
        'tasksLate':10,
    }
    return render(request,'dashboard/home.html',context)


