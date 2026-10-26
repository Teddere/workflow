from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.views.decorators.http import require_POST
from .forms import RegisterForm,LoginForm


def register_view(request):

    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('account:login')
    else:
        form = RegisterForm()
    return render(request, 'account/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            user = authenticate(
                request,email=form.cleaned_data['email'],
                password=form.cleaned_data['password']
            )
            if user is not None:
                login(request, user)
                return redirect('dashboard:home')
            messages.error(request, 'E-mail ou mot de passe incorrect !')
        else:
            messages.error(request, 'Veuillez entrer un email et un mot de passe !')

    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})

@require_POST
def logout_view(request):
    logout(request)
    return redirect('account:login')

