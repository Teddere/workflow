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
                    'class': 'w-full rounded-xl border p-3 text-sm',
                    'placeholder': 'Enter your username',
                }
            ),
            'email': forms.EmailInput(
                attrs={
                    'class': 'w-full rounded-xl border p-3 text-sm',
                    'placeholder': 'Enter your email',
                }
            ),
            'tel': forms.TextInput(
                attrs={
                    'type':'tel',
                    'class': 'w-full rounded-xl border p-3 text-sm',
                    'placeholder': 'Enter your phone number',
                }
            )
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({
            'class': 'w-full rounded-xl border p-3 text-sm',
            'placeholder': 'Enter your password',
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'w-full rounded-xl border p-3 text-sm',
            'placeholder': 'Confirm your password',
        })