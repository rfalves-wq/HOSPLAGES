from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from triagem.models import FilaTriagem
from medico.models import AtendimentoMedico
from .decorators import grupo_requerido

@login_required
@grupo_requerido(['Medico'])
def chamar_proximo_paciente(request):
    paciente_fila = FilaTriagem.objects.filter(
        triagem_realizada=True,
        encaminhado_medico=False
    ).order_by('data_entrada').first()

    if not paciente_fila:
        return render(request, 'medico/sem_paciente.html')

    atendimento = AtendimentoMedico.objects.create(
        paciente=paciente_fila.paciente,
        medico=request.user,
        queixa_principal=""
    )

    paciente_fila.encaminhado_medico = True
    paciente_fila.save()

    return redirect('atendimento_medico', atendimento.id)
@login_required
@grupo_requerido(['Medico'])
def chamar_proximo_paciente(request):
    paciente_fila = FilaTriagem.objects.filter(
        atendido=False
    ).order_by('data_entrada').first()

    if not paciente_fila:
        return render(request, 'medico/sem_paciente.html')

    atendimento = AtendimentoMedico.objects.create(
        paciente=paciente_fila.paciente,
        medico=request.user,
        queixa_principal=""
    )

    paciente_fila.atendido = True
    paciente_fila.save()

    return redirect('atendimento_medico', atendimento.id)

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from .models import AtendimentoMedico
@login_required
@grupo_requerido(['Medico'])
def atendimento_medico(request, atendimento_id):
    atendimento = get_object_or_404(AtendimentoMedico, id=atendimento_id)

    if request.method == 'POST':
        atendimento.queixa_principal = request.POST.get('queixa_principal')
        atendimento.historico_doenca_atual = request.POST.get('historico')
        atendimento.diagnostico = request.POST.get('diagnostico')
        atendimento.conduta = request.POST.get('conduta')
        atendimento.finalizado = True
        atendimento.data_fim = timezone.now()
        atendimento.save()

        return redirect('painel_medico')

    return render(request, 'medico/atendimento.html', {
        'atendimento': atendimento
    })

