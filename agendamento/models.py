from django.db import models
from django.conf import settings
from paciente.models import Paciente

class Agendamento(models.Model):
    STATUS_CHOICES = [
        ('AG', 'Agendado'),
        ('TR', 'Encaminhado para Triagem'),
        ('AT', 'Atendido'),
        ('CN', 'Cancelado'),
    ]

    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    data_hora = models.DateTimeField()
    encaminhado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default='AG')
    observacoes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.paciente} - {self.data_hora.strftime('%d/%m/%Y %H:%M')} - {self.get_status_display()}"
