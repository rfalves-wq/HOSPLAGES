from django.urls import path
from . import views

urlpatterns = [
    path('', views.agendamento_list, name='agendamento_list'),
    path('novo/', views.agendamento_create, name='agendamento_create'),
    path('triagem/<int:pk>/', views.enviar_triagem, name='enviar_triagem'),
    path('buscar_paciente/', views.buscar_paciente, name='buscar_paciente'),
]
