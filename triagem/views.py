from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from paciente.models import Paciente
from .models import Triagem, FilaTriagem
from .forms import TriagemForm


@login_required
def fila_triagem(request):
    # Pacientes aguardando TRIAGEM (ainda não triados)
    fila = FilaTriagem.objects.filter(atendido=False).order_by('data_entrada')

    # Contagem para dashboard
    total_pacientes = fila.count()
    
    # Quantidade por tempo de espera
    tempo_espera_0_5 = fila.filter(
        data_entrada__gte=timezone.now() - timezone.timedelta(minutes=5)
    ).count()

    tempo_espera_5_15 = fila.filter(
        data_entrada__lt=timezone.now() - timezone.timedelta(minutes=5),
        data_entrada__gte=timezone.now() - timezone.timedelta(minutes=15)
    ).count()

    tempo_espera_15_ = fila.filter(
        data_entrada__lt=timezone.now() - timezone.timedelta(minutes=15)
    ).count()

    # Tempo de espera formatado
    fila_formatada = []
    now = timezone.now()

    for item in fila:
        tempo_espera_min = int((now - item.data_entrada).total_seconds() // 60)
        horas = tempo_espera_min // 60
        minutos = tempo_espera_min % 60
        item.tempo_espera_horas = f"{horas}h {minutos}m"
        fila_formatada.append(item)

    return render(request, 'triagem/fila_triagem.html', {
        'fila': fila_formatada,
        'total_pacientes': total_pacientes,
        'tempo_espera_0_5': tempo_espera_0_5,
        'tempo_espera_5_15': tempo_espera_5_15,
        'tempo_espera_15_': tempo_espera_15_,
    })


@login_required
def realizar_triagem(request, paciente_id):
    paciente = get_object_or_404(Paciente, id=paciente_id)

    if request.method == 'POST':
        form = TriagemForm(request.POST)
        if form.is_valid():
            # Salva a triagem
            triagem = form.save(commit=False)
            triagem.paciente = paciente
            triagem.enfermeiro = request.user
            triagem.save()

            # Atualiza a fila:
            # - atendido = True → triagem realizada
            # - em_atendimento_medico continua False (médico ainda não chamou)
            fila_item = FilaTriagem.objects.filter(
                paciente=paciente,
                atendido=False
            ).first()

            if fila_item:
                fila_item.atendido = True
                fila_item.save()

            return redirect('fila_triagem')
    else:
        form = TriagemForm()

    return render(request, 'triagem/realizar_triagem.html', {
        'form': form,
        'paciente': paciente
    })
