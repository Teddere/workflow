from urllib.parse import uses_relative

from django import forms
from django.contrib.auth import get_user_model
from .models import Project

User = get_user_model()

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ('manager','title','description','status','start_date','end_date','members')
        widgets= {
            'manager':forms.Select(
                attrs={
                    'class':'capitalize w-full bg-transparent placeholder:text-zinc-400 text-zinc-700 text-sm border-zinc-200 border border-zinc-200 rounded-md pl-3 pr-8 py-2 transition duration-300 ease focus:outline-none focus:border-zinc-400 hover:border-zinc-400 shadow-sm focus:shadow appearance-none cursor-pointer',
                    'placeholder':'Responsable de projet'
                }
            ),
            'members':forms.CheckboxSelectMultiple(),
            'title':forms.TextInput(
                attrs={
                    'class':'w-full bg-transparent shadow-sm focus:shadow hover:border-zinc-300 placeholder:text-zinc-400 text-zinc-700 text-sm border border-zinc-200 rounded-md px-3 py-2 transition duration-300 ease focus:outline-none focus:border-zinc-400',
                    'placeholder':'Nom du project'
                }
            ),
            'description':forms.Textarea(
                attrs={
                    'class':'w-full bg-transparent resize-none shadow-sm focus:shadow hover:border-zinc-300 placeholder:text-zinc-400 text-zinc-700 text-sm border border-zinc-200 rounded-md px-3 py-2 transition duration-300 ease focus:outline-none focus:border-zinc-400',
                    'placeholder':'Description de projet',
                    'rows':4,
                }
            ),
            'status': forms.Select(
                attrs={
                    'class':'w-full bg-transparent placeholder:text-zinc-400 text-zinc-700 text-sm border-zinc-200 border border-zinc-200 rounded-md pl-3 pr-8 py-2 transition duration-300 ease focus:outline-none focus:border-zinc-400 hover:border-zinc-400 shadow-sm focus:shadow appearance-none cursor-pointer',
                    'placeholder':''
                }
            ),
            'start_date': forms.DateInput(
                attrs={
                    'type': 'date',
                    'class':'w-full bg-transparent resize-none shadow-sm focus:shadow hover:border-zinc-300 placeholder:text-zinc-400 text-zinc-700 text-sm border border-zinc-200 rounded-md px-3 py-2 transition duration-300 ease focus:outline-none focus:border-zinc-400',
                    'placeholder':'Date de début de projet'
                },
                format='%Y-%m-%d'
            ),
            'end_date': forms.DateInput(
                attrs= {
                    'type':'date',
                    'class':'w-full bg-transparent resize-none shadow-sm focus:shadow hover:border-zinc-300 placeholder:text-zinc-400 text-zinc-700 text-sm border border-zinc-200 rounded-md px-3 py-2 transition duration-300 ease focus:outline-none focus:border-zinc-400',
                    'placeholder': 'Date de fin de projet'
                },
                format='%Y-%m-%d'
            )

        }
        labels = {
            'manager':'Chef de projet',
            'title':'Titre',
            'description':'Description',
            'status':'Statut',
            'members':'Equipe',
            'start_date':'Début de projet',
            'end_date':'Fin de projet',
        }

    def __init__(self ,*args,user=None,**kwargs):
        super().__init__(*args, **kwargs)
        self.usr = user
        print('-------------------------------------------')
        print(self.usr.role)
        print('-------------------------------------------')

        active_users = User.objects.filter(is_active=True).order_by('username')

        self.fields['members'].queryset = active_users
        self.fields['manager'].empty_label = 'Sélectionner chef de projet'

        if user is not None and user.role == User.Role.MANAGER:
            self.fields['manager'].queryset = active_users.filter(pk=user.pk)
            self.fields['manager'].initial = user

    def clean_manager(self):
        manager = self.cleaned_data['manager']
        print('maintenant',self.usr.role)
        if self.usr is None:
            raise forms.ValidationError(
                "Impossible de déterminer l'utilisateur."
            )
        if self.usr.role == User.Role.MANAGER and manager.pk != self.usr.pk:
            raise forms.ValidationError(
                "Vous devez être responsable des projets que vous créez."
            )
        return manager