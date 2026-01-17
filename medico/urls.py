from django.urls import path
from . import views

urlpatterns = [
    path(
        'painel/',
        views.chamar_proximo_paciente,
        name='painel_medico'
    ),
    path(
        'atendimento/<int:atendimento_id>/',
        views.atendimento_medico,
        name='atendimento_medico'
    ),
]
