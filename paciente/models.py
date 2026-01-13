# paciente/models.py
from django.db import models
from django.core.validators import RegexValidator

class Paciente(models.Model):
    nome = models.CharField(max_length=100)
    cpf = models.CharField(
        max_length=14,
        unique=True,
        validators=[RegexValidator(r'^\d{3}\.\d{3}\.\d{3}-\d{2}$', 'CPF inválido! Use XXX.XXX.XXX-XX')]
    )
    data_nascimento = models.DateField()
    telefone = models.CharField(
        max_length=15,
        validators=[RegexValidator(r'^\(\d{2}\)\s\d{4,5}-\d{4}$', 'Telefone inválido! Use (XX) XXXXX-XXXX')]
    )
    email = models.EmailField(blank=True, null=True)
    endereco = models.TextField(blank=True, null=True)

    # Informações adicionais (como SUS)
    cartao_sus = models.CharField(max_length=18, blank=True, null=True)
    

    def __str__(self):
        return self.nome
