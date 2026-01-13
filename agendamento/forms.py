from django import forms
from .models import Agendamento

class AgendamentoForm(forms.ModelForm):
    data_hora = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'})
    )
    
    class Meta:
        model = Agendamento
        fields = ['paciente', 'data_hora', 'observacoes']
        widgets = {
            'paciente': forms.Select(attrs={'class': 'form-select'}),
            'observacoes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
