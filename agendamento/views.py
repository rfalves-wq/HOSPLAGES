# ==============================
# IMPORTS PADRÃO DJANGO
# ==============================
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils import timezone
from django.core.paginator import Paginator
from django.db.models import Count

# ==============================
# IMPORTS PYTHON
# ==============================
from collections import Counter

# ==============================
# IMPORTS DO PROJETO
# ==============================
from .models import Agendamento
from paciente.models import Paciente
from triagem.models import FilaTriagem


# ==============================
# LISTAGEM DE AGENDAMENTOS (com filtro, dashboard e paginação)
# ==============================
@login_required
def agendamento_list(request):
    hoje = timezone.localdate()
    data_filtro = request.GET.get('data')

    if data_filtro:
        agendamentos_qs = Agendamento.objects.filter(
            data_hora__date=data_filtro
        )
        data_template = data_filtro
    else:
        agendamentos_qs = Agendamento.objects.filter(
            data_hora__date=hoje
        )
        data_template = hoje.strftime('%Y-%m-%d')

    # Ordenação: mais recentes primeiro
    agendamentos_qs = agendamentos_qs.order_by('-data_hora')

    # Dashboard
    status_dict = dict(Counter(ag.status for ag in agendamentos_qs))
    total_agendamentos = agendamentos_qs.count()

    # Paginação
    paginator = Paginator(agendamentos_qs, 10)
    page_number = request.GET.get('page')
    agendamentos = paginator.get_page(page_number)

    return render(request, 'agendamento_list.html', {
        'agendamentos': agendamentos,
        'total_agendamentos': total_agendamentos,
        'status_dict': status_dict,
        'data_filtro': data_template,
    })

# ==============================
# CRIAR AGENDAMENTO (com validação básica)
# ==============================
@login_required
def agendamento_create(request):
    if request.method == 'POST':
        paciente_id = request.POST.get('paciente')
        data_hora = request.POST.get('data_hora')
        observacoes = request.POST.get('observacoes', '')

        if not paciente_id or not data_hora:
            return render(request, 'agendamento_form.html', {
                'erro': 'Paciente e data são obrigatórios.'
            })

        paciente = get_object_or_404(Paciente, pk=paciente_id)

        Agendamento.objects.create(
            paciente=paciente,
            data_hora=data_hora,
            observacoes=observacoes,
            encaminhado_por=request.user
        )

        return redirect('agendamento_list')

    return render(request, 'agendamento_form.html')

# ==============================
# ENVIAR PARA TRIAGEM (com bloqueio de duplicidade)
# ==============================
@login_required
def enviar_triagem(request, pk):
    agendamento = get_object_or_404(Agendamento, pk=pk)

    agendamento.status = 'TR'
    agendamento.save()

    if not FilaTriagem.objects.filter(
        paciente=agendamento.paciente,
        atendido=False
    ).exists():
        FilaTriagem.objects.create(paciente=agendamento.paciente)

    return redirect('agendamento_list')


# ==============================
# BUSCA DE PACIENTE (AUTOCOMPLETE)
# ==============================
@login_required
def buscar_paciente(request):
    term = request.GET.get('term', '')
    pacientes = Paciente.objects.filter(nome__icontains=term)[:10]

    resultados = [
        {
            'id': paciente.id,
            'label': f"{paciente.nome} - {paciente.cpf}",
            'value': paciente.nome
        }
        for paciente in pacientes
    ]

    return JsonResponse(resultados, safe=False)

# ==============================
# RELATÓRIO POR STATUS (dia / mês / ano)
# ==============================
@login_required
def relatorio_list(request):
    agendamentos = Agendamento.objects.all()

    dia = request.GET.get('dia')
    mes = request.GET.get('mes')
    ano = request.GET.get('ano')

    if dia:
        agendamentos = agendamentos.filter(data_hora__date=dia)
    if mes:
        agendamentos = agendamentos.filter(data_hora__month=mes)
    if ano:
        agendamentos = agendamentos.filter(data_hora__year=ano)

    status_count = Counter(ag.status for ag in agendamentos)
    status_display = dict(Agendamento.STATUS_CHOICES)

    relatorios = {
        status_display.get(status, status): qtd
        for status, qtd in status_count.items()
    }

    return render(request, 'relatorio_list.html', {
        'relatorios': relatorios,
        'dia': dia,
        'mes': mes,
        'ano': ano
    })

# ==============================
# RELATÓRIO DE AGENDAMENTOS POR DIA
# ==============================

@login_required
def agendamento_por_dia(request):
    agendamentos_dia = (
        Agendamento.objects
        .values('data_hora__date')
        .annotate(qtd=Count('id'))
        .order_by('data_hora__date')
    )

    return render(request, 'agendamento_por_dia.html', {
        'agendamentos_dia': agendamentos_dia
    })

