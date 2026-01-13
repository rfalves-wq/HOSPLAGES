# usuarios/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuario(AbstractUser):
    PERFIS = [
        ('recepcao', 'Recepção'),
        ('medico', 'Médico'),
        ('enfermeiro', 'Enfermeiro'),
        ('tecnico', 'Técnico'),
        ('administrador', 'Administrador'),
    ]
    perfil = models.CharField('Perfil', max_length=20, choices=PERFIS)

    def __str__(self):
        return f"{self.username} ({self.get_perfil_display()})"
