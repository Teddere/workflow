from django import forms
from .models import Project


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ('manager','title','description','members','status','start_date','end_date')
        widgets= {
            'manager':forms.Select(
                attrs={
                    'class':'w-full rounded-xl border p-3',
                    'placeholder':'Responsable de projet'
                }
            ),
            'members':forms.SelectMultiple(
                attrs={
                    'class':'w-full rounded-xl border p-3',
                    'placeholder':'Constituez une équipe'
                }
            ),
            'title':forms.TextInput(
                attrs={
                    'class':'w-full rounded-xl border p-3 text-sm',
                    'placeholder':'Nom du project'
                }
            ),
            'description':forms.Textarea(
                attrs={
                    'class':'w-full rounded-xl border p-3 outline focus:border-zinc-900',
                    'placeholder':'Description de projet'
                }
            ),
            'status': forms.Select(
                attrs={
                    'class':'w-full rounded-xl border p-3 text-sm',
                    'placeholder':''
                }
            ),
            'start_date': forms.DateInput(
                attrs={
                    'class':'w-full rounded-xl border p-3 text-sm lg:w-50',
                    'placeholder':'Date de début de projet'
                }
            ),
            'end_date': forms.DateInput(
                attrs= {
                    'class': 'w-full rounded-xl border p-3 text-sm lg:w-50',
                    'placeholder': 'Date de fin de projet'
                }
            )

        }