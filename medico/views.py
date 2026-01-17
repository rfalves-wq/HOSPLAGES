from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .decorators import grupo_requerido
from triagem.models import FilaTriagem
from medico.models import AtendimentoMedico

@login_required
@grupo_requerido(['Medico'])
def dashboard_medico(request):
    return render(request, 'medico/dashboard.html')

@login_required
@grupo_requerido(['Medico'])
@login_required
@grupo_requerido(['Medico'])
def lista_pacientes(request):
    # Pacientes na fila
    pacientes_fila = FilaTriagem.objects.filter(
        status__in=['aguardando_medico', 'em_atendimento']
    ).order_by('data_entrada')

    # Para cada paciente, pega a última triagem
    fila_formatada = []
    for item in pacientes_fila:
        ultima_triagem = Triagem.objects.filter(paciente=item.paciente).order_by('-data_triagem').first()
        item.triagem = ultima_triagem  # atributo temporário
        fila_formatada.append(item)

    return render(request, 'medico/lista_pacientes.html', {'pacientes_fila': fila_formatada})


@login_required
@grupo_requerido(['Medico'])
def chamar_proximo_paciente(request):
    paciente_fila = FilaTriagem.objects.filter(status='aguardando_medico').order_by('data_entrada').first()
    if not paciente_fila:
        return render(request, 'medico/sem_paciente.html')
    
    atendimento = AtendimentoMedico.objects.create(
        paciente=paciente_fila.paciente,
        medico=request.user,
        queixa_principal=""
    )
    
    paciente_fila.status = 'em_atendimento'
    paciente_fila.save()
    
    return redirect('medico:atendimento_medico', atendimento.id)

from django.shortcuts import render, get_object_or_404
from triagem.models import FilaTriagem
from medico.models import AtendimentoMedico
from django.shortcuts import render, get_object_or_404
from triagem.models import FilaTriagem
from medico.models import AtendimentoMedico
from django.contrib.auth.decorators import login_required
from .decorators import grupo_requerido
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import AtendimentoMedico
from triagem.models import FilaTriagem
from .decorators import grupo_requerido
from triagem.models import Triagem

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from medico.models import AtendimentoMedico
from triagem.models import Triagem
from .decorators import grupo_requerido

@login_required
@grupo_requerido(['Medico'])
def atendimento_medico(request, atendimento_id):
    atendimento = get_object_or_404(AtendimentoMedico, id=atendimento_id)

    # Pega a última triagem registrada do paciente
    triagem = Triagem.objects.filter(paciente=atendimento.paciente).order_by('-data_triagem').first()

    if request.method == "POST":
        # Atualiza os campos do atendimento
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
    atendimento.data_fim = timezone.now()
    atendimento.save()

    fila = FilaTriagem.objects.filter(paciente=atendimento.paciente, status='em_atendimento').first()
    if fila:
        fila.status = 'finalizado'
        fila.atendido = True
        fila.save()

    return redirect('medico:chamar_proximo_paciente')
