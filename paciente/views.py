from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

from .forms import PacienteForm
from .models import Paciente
from django.contrib.auth.decorators import login_required
from .decorators import grupo_requerido


# =========================
# CRIAR PACIENTE
# =========================
@login_required
@grupo_requerido(['Recepcao'])
def paciente_create(request):
    if request.method == 'POST':
        form = PacienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('paciente_list')
    else:
        form = PacienteForm()

    return render(request, 'paciente/form.html', {'form': form})


# =========================
# LISTAR PACIENTES
# =========================
@login_required
@grupo_requerido(['Recepcao', 'Enfermagem', 'Medico'])
def paciente_list(request):
    pacientes = Paciente.objects.all().order_by('nome')

    # Filtros de busca
    nome_query = request.GET.get('nome', '')
    cpf_query = request.GET.get('cpf', '')

    if nome_query:
        pacientes = pacientes.filter(nome__icontains=nome_query)
    if cpf_query:
        pacientes = pacientes.filter(cpf__icontains=cpf_query)

    # Paginação
    paginator = Paginator(pacientes, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'nome_query': nome_query,
        'cpf_query': cpf_query,
    }

    return render(request, 'paciente/list.html', context)


# =========================
# EDITAR PACIENTE
# =========================
@login_required
@grupo_requerido(['Recepcao'])
def paciente_edit(request, pk):
    paciente = get_object_or_404(Paciente, pk=pk)

    if request.method == 'POST':
        form = PacienteForm(request.POST, instance=paciente)
        if form.is_valid():
            form.save()
            return redirect('paciente_list')
    else:
        form = PacienteForm(instance=paciente)

    return render(request, 'paciente/form.html', {'form': form})
