from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from triagem.models import FilaTriagem
from medico.models import AtendimentoMedico
from .decorators import grupo_requerido


@login_required
@grupo_requerido(['Medico'])
def chamar_proximo_paciente(request):
    paciente_fila = (
        FilaTriagem.objects
        .filter(status='aguardando_medico')
        .order_by('data_entrada')
        .first()
    )

    if not paciente_fila:
        return render(request, 'medico/sem_paciente.html')

    # Cria atendimento médico
    atendimento = AtendimentoMedico.objects.create(
        paciente=paciente_fila.paciente,
        medico=request.user,
        queixa_principal=""
    )

    # Marca como em atendimento
    paciente_fila.status = 'em_atendimento'
    paciente_fila.save()

    return redirect('medico:atendimento_medico', atendimento.id)


@login_required
@grupo_requerido(['Medico'])
def atendimento_medico(request, atendimento_id):
    atendimento = get_object_or_404(AtendimentoMedico, id=atendimento_id)

    return render(request, 'medico/atendimento.html', {
        'atendimento': atendimento
    })


@login_required
@grupo_requerido(['Medico'])
def finalizar_atendimento(request, atendimento_id):
    atendimento = get_object_or_404(AtendimentoMedico, id=atendimento_id)

    atendimento.data_fim = timezone.now()
    atendimento.save()

    # Marca paciente como atendido
    fila = FilaTriagem.objects.filter(paciente=atendimento.paciente, status='em_atendimento').first()
    if fila:
        fila.status = 'finalizado'
        fila.atendido = True
        fila.save()

    return redirect('medico:chamar_proximo_paciente')
