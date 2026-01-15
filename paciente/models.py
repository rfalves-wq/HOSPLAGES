from django.db import models
from django.core.validators import RegexValidator

class Paciente(models.Model):

    # =====================
    # IDENTIFICAÇÃO BÁSICA
    # =====================
    nome = models.CharField(max_length=100)
    nome_social = models.CharField(max_length=100, blank=True, null=True)

    nome_mae = models.CharField(max_length=100)
    nome_pai = models.CharField(max_length=100, blank=True, null=True)

    cpf = models.CharField(
        max_length=14,
        unique=True,
        validators=[RegexValidator(
            r'^\d{3}\.\d{3}\.\d{3}-\d{2}$',
            'CPF inválido! Use XXX.XXX.XXX-XX'
        )]
    )

    data_nascimento = models.DateField()  # NÃO ALTERADO

    # =====================
    # DADOS SOCIODEMOGRÁFICOS
    # =====================
    SEXO_BIOLOGICO_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Feminino'),
        ('I', 'Intersexo'),
    ]
    sexo_biologico = models.CharField(max_length=1, choices=SEXO_BIOLOGICO_CHOICES)

    identidade_genero = models.CharField(max_length=50)
    orientacao_sexual = models.CharField(max_length=50)

    nacionalidade = models.CharField(max_length=50, default='Brasileira')
    naturalidade = models.CharField(max_length=100)  # Cidade / UF

    RACA_COR_CHOICES = [
        ('BRANCA', 'Branca'),
        ('PRETA', 'Preta'),
        ('PARDA', 'Parda'),
        ('AMARELA', 'Amarela'),
        ('INDIGENA', 'Indígena'),
    ]
    raca_cor = models.CharField(max_length=10, choices=RACA_COR_CHOICES)

    ESTADO_CIVIL_CHOICES = [
        ('SOLTEIRO', 'Solteiro(a)'),
        ('CASADO', 'Casado(a)'),
        ('DIVORCIADO', 'Divorciado(a)'),
        ('VIUVO', 'Viúvo(a)'),
        ('UNIAO_ESTAVEL', 'União Estável'),
    ]
    estado_civil = models.CharField(max_length=20, choices=ESTADO_CIVIL_CHOICES)

    escolaridade = models.CharField(max_length=50)
    profissao = models.CharField(max_length=50)

    # =====================
    # DOCUMENTOS
    # =====================
    rg = models.CharField(max_length=20)
    orgao_emissor = models.CharField(max_length=10)

    UF_CHOICES = [
        ('AC','AC'), ('AL','AL'), ('AP','AP'), ('AM','AM'),
        ('BA','BA'), ('CE','CE'), ('DF','DF'), ('ES','ES'),
        ('GO','GO'), ('MA','MA'), ('MT','MT'), ('MS','MS'),
        ('MG','MG'), ('PA','PA'), ('PB','PB'), ('PR','PR'),
        ('PE','PE'), ('PI','PI'), ('RJ','RJ'), ('RN','RN'),
        ('RS','RS'), ('RO','RO'), ('RR','RR'), ('SC','SC'),
        ('SP','SP'), ('SE','SE'), ('TO','TO'),
    ]
    uf_rg = models.CharField(max_length=2, choices=UF_CHOICES)

    # =====================
    # ENDEREÇO
    # =====================
    cep = models.CharField(
        max_length=9,
        validators=[RegexValidator(r'^\d{5}-\d{3}$', 'CEP inválido! Use XXXXX-XXX')]
    )
    endereco = models.CharField(max_length=100)
    numero = models.CharField(max_length=10)
    complemento = models.CharField(max_length=50, blank=True, null=True)
    bairro = models.CharField(max_length=50)
    municipio = models.CharField(max_length=50)
    uf = models.CharField(max_length=2, choices=UF_CHOICES)

    ZONA_CHOICES = [
        ('URBANA', 'Urbana'),
        ('RURAL', 'Rural'),
    ]
    zona = models.CharField(max_length=6, choices=ZONA_CHOICES)

    # =====================
    # CONTATO
    # =====================
    telefone_fixo = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        validators=[RegexValidator(
            r'^\(\d{2}\)\s\d{4}-\d{4}$',
            'Telefone inválido! Use (XX) XXXX-XXXX'
        )]
    )

    celular = models.CharField(
        max_length=15,
        validators=[RegexValidator(
            r'^\(\d{2}\)\s\d{5}-\d{4}$',
            'Celular inválido! Use (XX) XXXXX-XXXX'
        )]
    )

    whatsapp = models.BooleanField(default=False)
    email = models.EmailField(blank=True, null=True)

    # =====================
    # SUS
    # =====================
    cartao_sus = models.CharField(max_length=18, blank=True, null=True)

    def __str__(self):
        return self.nome
