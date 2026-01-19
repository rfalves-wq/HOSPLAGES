from django import forms
from .models import FilaTriagem

class TriagemForm(forms.ModelForm):
    class Meta:
        model = FilaTriagem
        fields = [
            'pressao_arterial', 'temperatura', 'frequencia_cardiaca',
            'saturacao', 'queixa_principal', 'observacoes', 'classificacao_risco'
        ]
