from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import FilaTriagem
from .forms import TriagemForm

def fila_triagem(request):
    # Pega todos os pacientes que ainda não foram atendidos
    fila = FilaTriagem.objects.filter(atendido=False).order_by('data_entrada')

    # Contadores para dashboard
    total_pacientes = fila.count()
    tempo_espera_0_5 = fila.filter(data_entrada__gte=timezone.now()-timezone.timedelta(minutes=5)).count()
    tempo_espera_15_ = fila.filter(data_entrada__lte=timezone.now()-timezone.timedelta(minutes=15)).count()

    return render(request, 'triagem/fila_triagem.html', {
        'fila': fila,
        'total_pacientes': total_pacientes,
        'tempo_espera_0_5': tempo_espera_0_5,
        'tempo_espera_15_': tempo_espera_15_,
    })
def realizar_triagem(request, paciente_id):
    fila = get_object_or_404(FilaTriagem, paciente_id=paciente_id, atendido=False)
    
    if request.method == 'POST':
        form = TriagemForm(request.POST, instance=fila)
        if form.is_valid():
            triagem = form.save(commit=False)
            triagem.tempo_espera = timezone.now() - fila.data_entrada
            triagem.atendido = True
            triagem.save()
            return redirect('fila_triagem')
    else:
        form = TriagemForm(instance=fila)
    
    return render(request, 'triagem/realizar_triagem.html', {
        'paciente': fila.paciente,
        'form': form
    })
