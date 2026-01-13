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


@login_required
def enviar_triagem(request, pk):
    agendamento = get_object_or_404(Agendamento, pk=pk)
    agendamento.status = 'TR'
    agendamento.save()
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
