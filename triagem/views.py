from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from paciente.models import Paciente
from .models import Triagem
from .forms import TriagemForm


@login_required
def fila_triagem(request):
    """
    Lista pacientes disponíveis para triagem
    (fluxo temporário enquanto não existe recepção)
    """
    pacientes = Paciente.objects.all()
    return render(request, 'triagem/fila_triagem.html', {
        'pacientes': pacientes
    })


@login_required
def realizar_triagem(request, paciente_id):
    paciente = get_object_or_404(Paciente, id=paciente_id)

    if request.method == 'POST':
        form = TriagemForm(request.POST)
        if form.is_valid():
            triagem = form.save(commit=False)
            triagem.paciente = paciente
            triagem.enfermeiro = request.user
            triagem.save()
            return redirect('fila_triagem')
    else:
        form = TriagemForm()

    return render(request, 'triagem/realizar_triagem.html', {
        'form': form,
        'paciente': paciente
    })
