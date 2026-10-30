from django import forms
from django.contrib.auth import get_user_model
from django.db.models import Q

from .models import Task
from apps.projects.models import Project

User = get_user_model()

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('title','description','project','assigned_to','status','priority','due_date')

        widgets = {
            'title': forms.TextInput(
                attrs={
                    'class': 'w-full bg-transparent text-zinc-700 text-sm border-zinc-200 border border-zinc-200 rounded-md pl-3 pr-8 py-2 transition duration-300 ease hover:border-zinc-400 shadow-sm focus:shadow appearance-none cursor-pointer placeholder:text-zinc-400 focus:outline-none focus:border-zinc-400',
                    'placeholder': 'Entrez un titre'
                }
            ),
            'description': forms.Textarea(
                attrs={
                    'class':'w-full bg-transparent resize-none shadow-sm focus:shadow hover:border-zinc-300 placeholder:text-zinc-400 text-zinc-700 text-sm border border-zinc-200 rounded-md px-3 py-2 transition duration-300 ease focus:outline-none focus:border-zinc-400',
                    'placeholder': 'Entrez une description'
                }
            ),
            'project': forms.Select(
                attrs={
                    'class':'w-full bg-transparent placeholder:text-zinc-400 text-zinc-700 text-sm border-zinc-200 border border-zinc-200 rounded-md pl-3 pr-8 py-2 transition duration-300 ease focus:outline-none focus:border-zinc-400 hover:border-zinc-400 shadow-sm focus:shadow appearance-none cursor-pointer'
                }
            ),
            'assigned_to': forms.Select(
                attrs={
                    'class':'w-full bg-transparent placeholder:text-zinc-400 text-zinc-700 text-sm border-zinc-200 border border-zinc-200 rounded-md pl-3 pr-8 py-2 transition duration-300 ease focus:outline-none focus:border-zinc-400 hover:border-zinc-400 shadow-sm focus:shadow appearance-none cursor-pointer'
                }
            ),
            'status': forms.Select(
                attrs={
                    'class':'w-full bg-transparent placeholder:text-zinc-400 text-zinc-700 text-sm border-zinc-200 border border-zinc-200 rounded-md pl-3 pr-8 py-2 transition duration-300 ease focus:outline-none focus:border-zinc-400 hover:border-zinc-400 shadow-sm focus:shadow appearance-none cursor-pointer'
                }
            ),
            'priority': forms.Select(
                attrs={
                    'class':'w-full bg-transparent placeholder:text-zinc-400 text-zinc-700 text-sm border-zinc-200 border border-zinc-200 rounded-md pl-3 pr-8 py-2 transition duration-300 ease focus:outline-none focus:border-zinc-400 hover:border-zinc-400 shadow-sm focus:shadow appearance-none cursor-pointer'
                }
            ),
            'due_date': forms.DateInput(
                attrs={
                    'type': 'date',
                    'class': 'w-full bg-transparent resize-none shadow-sm focus:shadow hover:border-zinc-300 placeholder:text-zinc-400 text-zinc-700 text-sm border border-zinc-200 rounded-md px-3 py-2 transition duration-300 ease focus:outline-none focus:border-zinc-400',
                },
                format='%Y-%m-%d'
            )
        }

    def __init__(self, *args,user=None,project=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        self.project = project
        # 1. Définir les projets autorisés
        projects = Project.objects.none()

        if user is not None:
            if user.role == User.Role.ADMIN:
                projects = Project.objects.all()
            elif user.role == User.Role.MANAGER:
                projects = Project.objects.filter(
                    manager=user
                )

        self.fields['project'].queryset = projects

        # 2. Aucun responsable disponible par défaut
        self.fields['assigned_to'].queryset = User.objects.none()

        #3. Déterminer le projet sélectionné
        selected_project = None

        if self.is_bound:
            project_id = self.data.get('project')

            selected_project = projects.filter(
                pk=project_id
            ).first() if project_id and str(project_id).isdigit() else None

        elif project is not None:
            selected_project = projects.filter(
                pk=project.pk
            ).first()
            if selected_project:
                self.fields['project'].initial = selected_project.pk

        elif self.instance.pk:
            selected_project = projects.filter(
                pk=self.instance.project_id
            ).first()
        # 4. Filtrer les utilisateurs selon le projet

        if selected_project is not None:
            self.fields['assigned_to'].queryset = User.objects.filter(
                Q(pk=selected_project.manager_id) | Q(projects=selected_project)
            ).filter(is_active=True).distinct()

    def clean(self):
        cleaned_data = super().clean()

        project = cleaned_data.get('project')
        assigned_to = cleaned_data.get('assigned_to')

        if project and assigned_to:

            is_manager = project.manager_id == assigned_to
            is_member = project.members.filter(pk=assigned_to).exists()
            if not (is_manager or is_member):
                self.add_error(
                    'assigned_to',"cet utilisateur n'appartient pas au projet"
                )

        return cleaned_data



