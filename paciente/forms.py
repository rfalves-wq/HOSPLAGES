# paciente/forms.py
from django import forms
from .models import Paciente
from django.core.exceptions import ValidationError
import re

class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = '__all__'
        widgets = {
            'data_nascimento': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'cpf': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'XXX.XXX.XXX-XX'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '(XX) XXXXX-XXXX'}),
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'endereco': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'cartao_sus': forms.TextInput(attrs={'class': 'form-control'}),
            
        }

    def clean_cpf(self):
        cpf = self.cleaned_data['cpf']
        if not re.match(r'^\d{3}\.\d{3}\.\d{3}-\d{2}$', cpf):
            raise ValidationError("CPF inválido! Use XXX.XXX.XXX-XX")
        return cpf

    def clean_telefone(self):
        telefone = self.cleaned_data['telefone']
        if not re.match(r'^\(\d{2}\)\s\d{4,5}-\d{4}$', telefone):
            raise ValidationError("Telefone inválido! Use (XX) XXXXX-XXXX")
        return telefone
