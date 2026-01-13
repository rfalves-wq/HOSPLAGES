# usuarios/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import LoginForm

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            usuario = form.get_user()
            login(request, usuario)
            # Redirecionar conforme o perfil
            if usuario.perfil == 'medico':
                return redirect('medico_dashboard')
            elif usuario.perfil == 'enfermeiro':
                return redirect('enfermeiro_dashboard')
            elif usuario.perfil == 'recepcao':
                return redirect('recepcao_dashboard')
            elif usuario.perfil == 'tecnico':
                return redirect('tecnico_dashboard')
            elif usuario.perfil == 'administrador':
                return redirect('admin_dashboard')
        else:
            messages.error(request, 'Usuário ou senha inválidos.')
    else:
        form = LoginForm()
    return render(request, 'usuarios/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

# Dashboards por perfil
@login_required
def medico_dashboard(request):
    return render(request, 'usuarios/medico.html')

@login_required
def enfermeiro_dashboard(request):
    return render(request, 'usuarios/enfermeiro.html')

@login_required
def recepcao_dashboard(request):
    return render(request, 'usuarios/recepcao.html')

@login_required
def tecnico_dashboard(request):
    return render(request, 'usuarios/tecnico.html')

@login_required
def admin_dashboard(request):
    return render(request, 'usuarios/admin.html')
