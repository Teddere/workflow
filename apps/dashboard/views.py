from django.shortcuts import render


def home(request):
    context = {
        'pageTitle':'Bienvenue sur TerWorkflow',
        'totalProjects':12,
        'totalTasks':48,
        'tasksCompleted':32,
        'tasksLate':10,
    }
    return render(request,'dashboard/home.html',context)
