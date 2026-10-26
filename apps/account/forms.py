from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username','email','tel')
        widgets = {
            'username': forms.TextInput(
                attrs={
                    'class':'w-full rounded-xl border p-3 text-sm',
                    'placeholder': 'Entrez votre nom utilisateur',
                }),
            'email': forms.EmailInput(
                attrs={
                    'class':'w-full rounded-xl border p-3 text-sm',
                    'placeholder': 'Entrez votre email',
                }
            ),
            'tel': forms.TextInput(
                attrs={
                    'type':'tel',
                    'class':'w-full rounded-xl border p-3 text-sm',
                    'placeholder': 'Entrez votre numéro de téléphone'
                }
            )
        }
        labels = {
            'tel':'Téléphone',
            'email':'E-mail',
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({
            'class':'w-full rounded-xl border p-3 text-sm',
            'placeholder':'Entrez votre mot de passe'
        })
        self.fields['password2'].widget.attrs.update({
            'class':'w-full rounded-xl border p-3 text-sm',
            'placeholder':'Confirmez votre mot de passe'
        })


class LoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                'class': 'w-full rounded-xl border p-3 text-sm',
                'placeholder': 'Entrez votre email',
                'autocomplete': 'email'
            }
        )
    )

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'w-full rounded-xl border p-3',
                'placeholder': 'Entrez votre mot de passe',
                'autocomplete': 'password',
            }
        )

    )
