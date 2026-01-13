# paciente/views.py
from django.shortcuts import render, redirect
from .forms import PacienteForm
from .models import Paciente

def paciente_create(request):
    if request.method == 'POST':
        form = PacienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('paciente_list')
    else:
        form = PacienteForm()
    return render(request, 'paciente/form.html', {'form': form})

# views.py
from django.shortcuts import render
from .models import Paciente

# views.py
from django.core.paginator import Paginator
from django.shortcuts import render
from .models import Paciente

def paciente_list(request):
    pacientes = Paciente.objects.all().order_by('nome')  # Ordena por nome
    
    # Filtros de busca
    nome_query = request.GET.get('nome', '')
    cpf_query = request.GET.get('cpf', '')

    if nome_query:
        pacientes = pacientes.filter(nome__icontains=nome_query)
    if cpf_query:
        pacientes = pacientes.filter(cpf__icontains=cpf_query)
    
    # Paginação
    paginator = Paginator(pacientes, 10)  # 10 pacientes por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'nome_query': nome_query,
        'cpf_query': cpf_query,
    }
    return render(request, 'paciente/list.html', context)




# views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import Paciente
from .forms import PacienteForm

def paciente_edit(request, pk):
    paciente = get_object_or_404(Paciente, pk=pk)
    if request.method == "POST":
        form = PacienteForm(request.POST, instance=paciente)
        if form.is_valid():
            form.save()
            return redirect('paciente_list')
    else:
        form = PacienteForm(instance=paciente)
    return render(request, 'paciente/form.html', {'form': form})
