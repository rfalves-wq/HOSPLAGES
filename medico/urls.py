from django.urls import path
from . import views

app_name = 'medico'

urlpatterns = [
    # Painel / chamar próximo paciente
    path('chamar/', views.chamar_proximo_paciente, name='chamar_proximo_paciente'),

    # Tela de atendimento médico
    path('atendimento/<int:atendimento_id>/', views.atendimento_medico, name='atendimento_medico'),

    # Finalizar atendimento
    path('finalizar/<int:atendimento_id>/', views.finalizar_atendimento, name='finalizar_atendimento'),
]
