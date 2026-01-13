# usuarios/urls.py
from django.urls import path
from .views import login_view, logout_view, medico_dashboard, enfermeiro_dashboard, recepcao_dashboard, tecnico_dashboard, admin_dashboard

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('medico/', medico_dashboard, name='medico_dashboard'),
    path('enfermeiro/', enfermeiro_dashboard, name='enfermeiro_dashboard'),
    path('recepcao/', recepcao_dashboard, name='recepcao_dashboard'),
    path('tecnico/', tecnico_dashboard, name='tecnico_dashboard'),
    path('administrador/', admin_dashboard, name='admin_dashboard'),
]
