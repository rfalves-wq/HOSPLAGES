from django.contrib import admin
from .models import Paciente

@admin.register(Paciente)
class PacienteAdmin(admin.ModelAdmin):
    # Campos exibidos na lista de pacientes
    list_display = (
        'nome', 'cpf', 'data_nascimento', 'sexo_biologico',
        'raca_cor', 'escolaridade', 'municipio', 'uf', 'cartao_sus'
    )

    # Campos que podem ser filtrados na lateral
    list_filter = (
        'sexo_biologico', 'raca_cor', 'escolaridade',
        'estado_civil', 'uf', 'zona'
    )

    # Campos que podem ser buscados
    search_fields = ('nome', 'cpf', 'cartao_sus', 'nome_mae')

    # Organização dos campos no formulário do admin
    fieldsets = (
        ('Dados Pessoais', {
            'fields': (
                'nome', 'nome_social', 'nome_mae', 'nome_pai',
                'cpf', 'data_nascimento', 'sexo_biologico',
                'identidade_genero', 'orientacao_sexual',
                'nacionalidade', 'naturalidade', 'raca_cor',
                'estado_civil', 'escolaridade', 'profissao'
            )
        }),
        ('Documentos', {
            'fields': ('rg', 'orgao_emissor', 'uf_rg')
        }),
        ('Endereço', {
            'fields': (
                'endereco', 'numero', 'complemento', 'bairro',
                'municipio', 'uf', 'zona', 'cep'
            )
        }),
        ('Contato', {
            'fields': ('telefone_fixo', 'celular', 'whatsapp', 'email')
        }),
        ('SUS / Convênio', {
            'fields': ('cartao_sus', 'convenio')
        }),
    )

    # Ordenação padrão na lista
    ordering = ('nome',)

    # Número de registros por página
    list_per_page = 25
