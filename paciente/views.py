from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from .forms import PacienteForm
from .models import Paciente


# =========================
# CRIAR PACIENTE
# =========================
def paciente_create(request):
    if request.method == 'POST':
        form = PacienteForm(request.POST)
        if form.is_valid():
            paciente = form.save(commit=False)
            paciente.criado_por = request.user  # AUDITORIA
            paciente.save()
            return redirect('paciente_list')
    else:
        form = PacienteForm()

    return render(request, 'paciente/form.html', {'form': form})


# =========================
# LISTAR PACIENTES
# =========================
def paciente_list(request):
    pacientes = Paciente.objects.all().order_by('nome')

    # Filtros
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
def paciente_edit(request, pk):
    paciente = get_object_or_404(Paciente, pk=pk)

    if request.method == 'POST':
        form = PacienteForm(request.POST, instance=paciente)
        if form.is_valid():
            form.save()  # NÃO altera criado_por
            return redirect('paciente_list')
    else:
        form = PacienteForm(instance=paciente)

    return render(request, 'paciente/form.html', {'form': form})
