from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.utils.timezone import localtime

from .decorators import grupo_requerido
from triagem.models import FilaTriagem, Triagem
from medico.models import AtendimentoMedico

@login_required
@grupo_requerido(['Medico'])
def dashboard_medico(request):
    fila = FilaTriagem.objects.filter(atendido=False).order_by('data_entrada')
    now = timezone.localtime(timezone.now())

    total_pacientes = fila.count()
    tempo_espera_0_5 = fila.filter(data_entrada__gte=now - timezone.timedelta(minutes=5)).count()
    tempo_espera_5_15 = fila.filter(
        data_entrada__lt=now - timezone.timedelta(minutes=5),
        data_entrada__gte=now - timezone.timedelta(minutes=15)
    ).count()
    tempo_espera_15_ = fila.filter(data_entrada__lt=now - timezone.timedelta(minutes=15)).count()

    fila_formatada = []
    for item in fila:
        ultima_triagem = Triagem.objects.filter(paciente=item.paciente).order_by('-data_triagem').first()
        item.triagem = ultima_triagem

        if ultima_triagem:
            item.data_entrada_local = localtime(ultima_triagem.data_triagem)
            diff_min = int((now - ultima_triagem.data_triagem).total_seconds() // 60)
        else:
            item.data_entrada_local = localtime(item.data_entrada)
            diff_min = int((now - item.data_entrada).total_seconds() // 60)

        horas = diff_min // 60
        minutos = diff_min % 60
        item.tempo_espera_horas = f"{horas}h {minutos}m"

        fila_formatada.append(item)

    return render(request, 'medico/dashboard.html', {
        'fila': fila_formatada,
        'total_pacientes': total_pacientes,
        'tempo_espera_0_5': tempo_espera_0_5,
        'tempo_espera_5_15': tempo_espera_5_15,
        'tempo_espera_15_': tempo_espera_15_,
    })

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.utils.timezone import localtime

from .decorators import grupo_requerido
from triagem.models import FilaTriagem, Triagem
from medico.models import AtendimentoMedico
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.utils.timezone import localtime
from .decorators import grupo_requerido
from triagem.models import FilaTriagem, Triagem

@login_required
@grupo_requerido(['Medico'])
def lista_pacientes(request):
    # Lista todos os pacientes, mesmo com atendido=True ou data_entrada vazia
    pacientes_fila = FilaTriagem.objects.all().order_by('data_entrada')
    now = timezone.localtime(timezone.now())
    fila_formatada = []

    for item in pacientes_fila:
        # Última triagem
        ultima_triagem = Triagem.objects.filter(paciente=item.paciente).order_by('-data_triagem').first()
        item.triagem = ultima_triagem

        # Hora de chegada
        if ultima_triagem and ultima_triagem.data_triagem:
            item.data_entrada_local = localtime(ultima_triagem.data_triagem)
            diff_min = int((now - ultima_triagem.data_triagem).total_seconds() // 60)
        elif item.data_entrada:
            item.data_entrada_local = localtime(item.data_entrada)
            diff_min = int((now - item.data_entrada).total_seconds() // 60)
        else:
            item.data_entrada_local = None
            diff_min = None

        # Tempo de espera
        if diff_min is not None:
            horas = diff_min // 60
            minutos = diff_min % 60
            item.tempo_espera_horas = f"{horas}h {minutos}m"
        else:
            item.tempo_espera_horas = "--:--"

        fila_formatada.append(item)

    return render(request, 'medico/lista_pacientes.html', {
        'pacientes': fila_formatada
    })


@login_required
@grupo_requerido(['Medico'])
def chamar_proximo_paciente(request):
    paciente_fila = FilaTriagem.objects.filter(atendido=False).order_by('data_entrada').first()
    if not paciente_fila:
        return render(request, 'medico/sem_paciente.html')

    atendimento = AtendimentoMedico.objects.create(
        paciente=paciente_fila.paciente,
        medico=request.user,
        queixa_principal=""
    )

    paciente_fila.atendido = True
    paciente_fila.save()

    return redirect('medico:atendimento_medico', atendimento.id)


@login_required
@grupo_requerido(['Medico'])
def atendimento_medico(request, atendimento_id):
    atendimento = get_object_or_404(AtendimentoMedico, id=atendimento_id)
    triagem = Triagem.objects.filter(paciente=atendimento.paciente).order_by('-data_triagem').first()

    if request.method == "POST":
        atendimento.queixa_principal = request.POST.get('queixa_principal', '')
        atendimento.historico_doenca_atual = request.POST.get('historico', '')
        atendimento.diagnostico = request.POST.get('diagnostico', '')
        atendimento.conduta = request.POST.get('conduta', '')
        atendimento.save()

    return render(request, 'medico/atendimento.html', {
        'atendimento': atendimento,
        'triagem': triagem
    })


@login_required
@grupo_requerido(['Medico'])
def finalizar_atendimento(request, atendimento_id):
    atendimento = get_object_or_404(AtendimentoMedico, id=atendimento_id)
    atendimento.data_fim = timezone.localtime(timezone.now())
    atendimento.save()

    fila = FilaTriagem.objects.filter(paciente=atendimento.paciente, atendido=True).first()
    if fila:
        fila.atendido = True
        fila.save()

    return redirect('medico:chamar_proximo_paciente')
