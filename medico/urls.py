from django.urls import path
from . import views

app_name = 'medico'  # Importante para usar {% url 'medico:...' %}

urlpatterns = [
    path('', views.dashboard_medico, name='dashboard'),  # Dashboard principal
    path('lista_pacientes/', views.lista_pacientes, name='lista_pacientes'),  # Lista de pacientes
    path('chamar/', views.chamar_proximo_paciente, name='chamar_proximo_paciente'),  # Chamar próximo paciente
    path('atendimento/<int:atendimento_id>/', views.atendimento_medico, name='atendimento_medico'),  # Tela de atendimento
    path('finalizar/<int:atendimento_id>/', views.finalizar_atendimento, name='finalizar_atendimento'),  # Finalizar atendimento
]
