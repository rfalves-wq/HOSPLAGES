from django.urls import path
from . import views

urlpatterns = [
    path('fila/', views.fila_triagem, name='fila_triagem'),
    path('realizar/<int:paciente_id>/', views.realizar_triagem, name='realizar_triagem'),
]
