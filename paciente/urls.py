# paciente/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.paciente_list, name='paciente_list'),
    path('novo/', views.paciente_create, name='paciente_create'),
    path('pacientes/<int:pk>/editar/', views.paciente_edit, name='paciente_edit'),
   
]
