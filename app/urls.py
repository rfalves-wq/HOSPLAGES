from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('usuarios.urls')),
    path('pacientes/', include('paciente.urls')),
path('agendamento/', include('agendamento.urls')),
path('triagem/', include('triagem.urls')),
path('medico/', include('medico.urls')),


]
from django.conf.urls import handler403
from django.shortcuts import render

def custom_403_view(request, exception=None):
    return render(request, '403.html', status=403)

handler403 = custom_403_view