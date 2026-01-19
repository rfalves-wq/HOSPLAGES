from django.db import models
from django.conf import settings
from django.utils import timezone
from paciente.models import Paciente

from django.db import models
from paciente.models import Paciente
from django.db import models
from paciente.models import Paciente
from django.utils import timezone

class FilaTriagem(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    data_entrada = models.DateTimeField(default=timezone.now)  # hora de chegada
    atendido = models.BooleanField(default=False)
    # Campos da triagem
    pressao_arterial = models.CharField(max_length=20, blank=True, null=True)
    temperatura = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True)
    frequencia_cardiaca = models.IntegerField(blank=True, null=True)
    saturacao = models.IntegerField(blank=True, null=True)
    queixa_principal = models.TextField(blank=True, null=True)
    observacoes = models.TextField(blank=True, null=True)
    classificacao_risco = models.CharField(max_length=10, choices=[('VERMELHO','Vermelho'), ('AMARELO','Amarelo'), ('VERDE','Verde')], blank=True, null=True)
    tempo_espera = models.DurationField(blank=True, null=True)  # tempo até a triagem

    def __str__(self):
        return f"{self.paciente.nome} - {'Atendido' if self.atendido else 'Aguardando'}"



class Triagem(models.Model):
    CLASSIFICACAO_RISCO = [
        ('VERMELHO', 'Vermelho - Emergência'),
        ('LARANJA', 'Laranja - Muito Urgente'),
        ('AMARELO', 'Amarelo - Urgente'),
        ('VERDE', 'Verde - Pouco Urgente'),
        ('AZUL', 'Azul - Não Urgente'),
    ]

    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    enfermeiro = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True
    )

    pressao_arterial = models.CharField(max_length=20)
    frequencia_cardiaca = models.IntegerField()
    temperatura = models.DecimalField(max_digits=4, decimal_places=1)
    saturacao = models.IntegerField()

    queixa_principal = models.TextField()
    observacoes = models.TextField(blank=True)

    classificacao_risco = models.CharField(
        max_length=10,
        choices=CLASSIFICACAO_RISCO
    )

    data_triagem = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.paciente.nome} - {self.classificacao_risco}'
