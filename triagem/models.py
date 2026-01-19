from django.db import models
from django.conf import settings
from django.utils import timezone
from paciente.models import Paciente

from django.db import models
from paciente.models import Paciente

class FilaTriagem(models.Model):
    STATUS_CHOICES = [
        ('aguardando_medico', 'Aguardando Médico'),
        ('em_atendimento', 'Em Atendimento'),
        ('finalizado', 'Finalizado'),
    ]

    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    data_entrada = models.DateTimeField(auto_now_add=True)
    atendido = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='aguardando_medico')

    def __str__(self):
        return f"{self.paciente.nome} - {self.status}"


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
