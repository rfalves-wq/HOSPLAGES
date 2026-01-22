from django.db import models
from django.conf import settings
from paciente.models import Paciente


class AtendimentoMedico(models.Model):
    paciente = models.ForeignKey(
        Paciente,
        on_delete=models.CASCADE,
        related_name='atendimentos'
    )
    medico = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='atendimentos_medicos'
    )

    queixa_principal = models.TextField()
    historico_doenca_atual = models.TextField(blank=True)
    diagnostico = models.TextField(blank=True)
    conduta = models.TextField(blank=True)

    # Novos campos
    fila = models.IntegerField(default=0)
    status = models.CharField(max_length=50, default='aguardando')

    data_inicio = models.DateTimeField(auto_now_add=True)
    data_fim = models.DateTimeField(null=True, blank=True)
    finalizado = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.paciente.nome} - {self.medico.username}"


class FilaTriagem(models.Model):
    paciente = models.ForeignKey(
        Paciente,
        on_delete=models.CASCADE,
        related_name='filas_medico'
    )
    data_entrada = models.DateTimeField(auto_now_add=True)
    atendido = models.BooleanField(default=False)

