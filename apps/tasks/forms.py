from django import forms
from django.contrib.auth import get_user_model
from django.db.models import Q

from .models import Task
from apps.projects.models import Project

User = get_user_model()

class TaskForm(forms.ModelForm):
    def __init__(self, *args,user=None,project=None, **kwargs):
        super().__init__(*args, **kwargs)

        self.user = user
        self.project = project


        self.fields['assigned_to'].queryset = User.objects.none()

        if project is not None:
            self.fields['assigned_to'].queryset = project.members.all()

    class Meta:
        model = Task
        fields = ('title','priority','assigned_to','status','due_date','description')

        widgets = {
            'title': forms.TextInput(
                attrs={
                    'class': 'w-full bg-transparent text-zinc-700 text-sm border border-zinc-200 rounded-md pl-3 pr-8 py-2 transition duration-300 ease hover:border-zinc-400 shadow-sm focus:shadow appearance-none cursor-pointer placeholder:text-zinc-400 focus:outline-none focus:border-zinc-400',
                    'placeholder': 'Entrez un titre'
                }
            ),
            'description': forms.Textarea(
                attrs={
                    'class':'w-full bg-transparent resize-none shadow-sm focus:shadow hover:border-zinc-300 placeholder:text-zinc-400 text-zinc-700 text-sm border border-zinc-200 rounded-md px-3 py-2 transition duration-300 ease focus:outline-none focus:border-zinc-400',
                    'placeholder': 'Entrez une description',
                    'rows':4
                }
            ),
            'assigned_to': forms.Select(
                attrs={
                    'class':'w-full bg-transparent placeholder:text-zinc-400 text-zinc-700 text-sm border border-zinc-200 rounded-md pl-3 pr-8 py-2 transition duration-300 ease focus:outline-none focus:border-zinc-400 hover:border-zinc-400 shadow-sm focus:shadow appearance-none cursor-pointer'
                }
            ),
            'status': forms.Select(
                attrs={
                    'class':'w-full bg-transparent placeholder:text-zinc-400 text-zinc-700 text-sm  border border-zinc-200 rounded-md pl-3 pr-8 py-2 transition duration-300 ease focus:outline-none focus:border-zinc-400 hover:border-zinc-400 shadow-sm focus:shadow appearance-none cursor-pointer'
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
        labels = {
            'title':'Titre',
            'priority':"Niveau d'urgence",
            'description':'Description',
            'project':'Projet',
            'assigned_to':'Responsable',
            'status':'État',
            'due_date':'Date échéance'
        }

    def clean(self):
        cleaned_data = super().clean()
        due_date = cleaned_data.get('due_date')

        if (self.project is not None and due_date and self.project.start_date):

            if due_date < self.project.start_date:
                self.add_error('due_date','La date limite ne peut pas précéder le début du projet. ')

        return cleaned_data

class TaskStatusForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('status',)
        widgets = {
            'status': forms.Select(
                attrs={
                    'class':'w-full bg-transparent placeholder:text-zinc-400 text-zinc-700 text-sm  border border-zinc-200 rounded-md pl-3 pr-8 py-2 transition duration-300 ease focus:outline-none focus:border-zinc-400 hover:border-zinc-400 shadow-sm focus:shadow appearance-none cursor-pointer'
                }
            )
        }

        labels = {
            'status':'Statut de la tâche',
        }



