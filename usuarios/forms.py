# usuarios/forms.py
from django import forms
from django.contrib.auth.forms import AuthenticationForm

class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label='Usuário',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite seu usuário'}),
        error_messages={'required': 'O campo usuário é obrigatório.'}
    )
    password = forms.CharField(
        label='Senha',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Digite sua senha'}),
        error_messages={'required': 'O campo senha é obrigatório.'}
    )
