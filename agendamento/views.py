from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Agendamento
from .forms import AgendamentoForm

@login_required
def agendamento_list(request):
    agendamentos = Agendamento.objects.all().order_by('data_hora')
    return render(request, 'agendamento_list.html', {'agendamentos': agendamentos, 'user': request.user})

# agendamento/views.py
from paciente.models import Paciente

@login_required
def agendamento_create(request):
    if request.method == 'POST':
        paciente_id = request.POST.get('paciente')
        paciente = Paciente.objects.get(pk=paciente_id)
        data_hora = request.POST.get('data_hora')
        observacoes = request.POST.get('observacoes', '')

        Agendamento.objects.create(
            paciente=paciente,
            data_hora=data_hora,
            observacoes=observacoes,
            encaminhado_por=request.user
        )
        return redirect('agendamento_list')

    return render(request, 'agendamento_form.html', {'user': request.user})

from django.shortcuts import redirect, get_object_or_404
from .models import Agendamento
from triagem.models import FilaTriagem  # importar o modelo da fila

@login_required
def enviar_triagem(request, pk):
    agendamento = get_object_or_404(Agendamento, pk=pk)

    # Atualiza o status do agendamento
    agendamento.status = 'TR'
    agendamento.save()

    # Verifica se já existe na fila para não duplicar
    fila_existente = FilaTriagem.objects.filter(paciente=agendamento.paciente, atendido=False).exists()
    if not fila_existente:
        FilaTriagem.objects.create(paciente=agendamento.paciente)

    return redirect('agendamento_list')


# agendamento/views.py
from django.http import JsonResponse
from paciente.models import Paciente
from django.contrib.auth.decorators import login_required

@login_required
def buscar_paciente(request):
    term = request.GET.get('term', '')
    pacientes = Paciente.objects.filter(nome__icontains=term)[:10]
    resultados = []
    for paciente in pacientes:
        resultados.append({
            'id': paciente.id,
            'label': f"{paciente.nome} - {paciente.cpf}",  # Pode mostrar CPF ou outro dado
            'value': paciente.nome
        })
    return JsonResponse(resultados, safe=False)

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from collections import Counter
from .models import Agendamento

@login_required
def relatorio_list(request):
    agendamentos = Agendamento.objects.all()

    # Receber filtros do GET
    dia = request.GET.get('dia')
    mes = request.GET.get('mes')
    ano = request.GET.get('ano')

    # Filtro por DIA (data completa)
    if dia:
        agendamentos = agendamentos.filter(data_hora__date=dia)

    # Filtro por MÊS
    if mes:
        agendamentos = agendamentos.filter(data_hora__month=mes)

    # Filtro por ANO
    if ano:
        agendamentos = agendamentos.filter(data_hora__year=ano)

    # Contagem por status
    status_count = Counter(ag.status for ag in agendamentos)

    # Converter status para texto
    status_display = dict(Agendamento.STATUS_CHOICES)
    relatorios = {
        status_display.get(status, status): quantidade
        for status, quantidade in status_count.items()
    }

    return render(request, 'relatorio_list.html', {
        'relatorios': relatorios,
        'dia': dia,
        'mes': mes,
        'ano': ano
    })
