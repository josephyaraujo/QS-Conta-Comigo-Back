from datetime import date, timedelta

from django.db import models # type: ignore
from django.contrib.auth.models import AbstractUser # type: ignore
from django.conf import settings # type: ignore
from django.core.exceptions import ValidationError  # type: ignore
from .utils import Utilitaria
from django.utils import timezone 

from .choices import *

class Usuario(AbstractUser):
    nome_completo = models.CharField(max_length=100, verbose_name="Nome Completo")

    def __str__(self):
        return self.nome_completo
    
    def clean(self):
        erros={}
        if len(self.username) < 3:
            erros['username']="O nome de usuário deve ter pelo menos 3 caracteres."
        if len(self.nome_completo) < 10:
            erros['nome']="O nome completo deve ter pelo menos 10 caracteres."
        if erros:
            raise ValidationError(erros)
        
    @property
    def tipo(self):
        if Aluno.objects.filter(usuario=self).exists():
            return 'aluno'
        elif AssistenteSocial.objects.filter(usuario=self).exists():
            return 'assistente_social'
        elif self.is_superuser:
            return 'admin'
        return 'desconhecido'

        
class Aluno(models.Model):
    usuario = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    matricula = models.CharField(max_length=14,unique=True, verbose_name="Matrícula")
    cpf = models.CharField(max_length=11, unique=True, verbose_name="CPF")
    curso = models.CharField(max_length=300, choices=CURSOS_IFRN_NATAL_CENTRAL, verbose_name="Curso") # TODO: transformar isso em id para relacionar com a tabela cursos para permitir filtrar
    periodo = models.IntegerField(verbose_name="Período")
    status = models.CharField(max_length=100)
    campus = models.CharField(max_length=100, null=False, blank=False, default = 'Natal-Central')
    ingresso = models.CharField(max_length=100, null=True, blank=True) # essa informação nao é passada pelo suap e nem muito usada nas regras do nosso sistema, TODO: tirar
    qtd_periodos = models.IntegerField(null=True, blank=True)

    def cpf_formatado(self):
        """Retorna o CPF formatado como XXX.XXX.XXX-XX."""
        if self.cpf:
            return Utilitaria.formatar_cpf(self.cpf)
        return self.cpf
    
    def __str__(self):
        return self.matricula
    
    def clean(self):
        erros={}
        if len(self.matricula) != 14:
            erros['matricula']="A matrícula do aluno deve ter 14 digitos."
        if self.periodo is None or not isinstance(self.periodo, int):
            erros['periodo'] = "O período precisa ser um número inteiro."
        elif self.periodo < 1:
            erros['periodo']="O período precisa ser maior ou igual a 1."
        if len(self.cpf) != 11 or not self.cpf.isdigit():
            erros['cpf']="O CPF deve ter 11 dígitos numéricos."
        if erros:
            raise ValidationError(erros)
        
    @property
    def full_name(self):
        return self.usuario.nome_completo
    
    @property
    def documentos(self):
        documentos = Documento.objects.filter(aluno=self)
        return documentos
        
class AssistenteSocial(models.Model):
    usuario = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='assistentesocial')
    matricula = models.CharField(max_length=7, unique=True, verbose_name="Matrícula")
    
    def __str__(self):
        return self.matricula

    
    def clean(self):
        erros={}
        if len(self.matricula) != 7:
            erros['matricula']="A matrícula da assistente social deve ter exatamente 7 dígitos."
        if erros:
            raise ValidationError(erros)

         
class Formulario(models.Model):
    titulo = models.CharField(max_length=100, null=False, blank=False)
    objetivo = models.TextField()
    solicitados = models.CharField(max_length=30, choices=SOLICITADOS_CHOICES, default="todos")
    # retirei o campo 'tipo' porque o campo auxilio_alvo já cumpre essa função e ele não precisa vir do choices e sim ser uma fk para o modelo Auxilio
    auxilio_alvo = models.ForeignKey('Auxilio', on_delete=models.CASCADE, null=True, blank=True, related_name='formularios_alvo', verbose_name="Auxílio Alvo") #apenas se for enviar para alunos do auxílio selecionado
    alunos_selecionados = models.ManyToManyField('Aluno', blank=True, related_name='formularios_individuais', verbose_name="Alunos Selecionados"
    ) #apenas se o tipo for "individual"
    data_inicio = models.DateField()
    data_fim = models.DateField()
    alunos_solicitados = models.IntegerField(default=0)
    status = models.CharField(max_length=20, choices=STATUS_FORMULARIO_CHOICES, default='rascunho')
    
    def __str__(self):
        return f"{self.titulo} - {self.objetivo}"
    
    def save(self, *args, **kwargs):
        # Atualiza automaticamente o status baseado na data_fim
        from django.utils import timezone
        hoje = timezone.now().date()
        
        # Se passou da data_fim e não está em rascunho, marca como concluído
        if self.data_fim < hoje and self.status != 'rascunho':
            self.status = 'concluido'
        # Se está entre data_inicio e data_fim e não está em rascunho, marca como aberto
        elif self.data_inicio <= hoje <= self.data_fim and self.status == 'concluido':
            self.status = 'aberto'
            
        super().save(*args, **kwargs)
    
    def clean(self):
        erros = {}
        if not self.titulo: 
            erros['titulo'] = "O formulário deve ter um título."
            
        if self.data_fim < self.data_inicio:
            erros['data_fim'] = "A data final do formulário não pode ser menor que a data inicial."
            
        if self.solicitados == 'auxilio' and not self.auxilio_alvo: 
            erros['auxilio_alvo'] = "O modo 'Auxílio Específico' exige a seleção de um Auxílio."
        
        if erros:
            raise ValidationError(erros)
        
    class Meta:
        db_table = 'formulario'
    
class FormularioQuestao(models.Model):
    formulario = models.ForeignKey('Formulario', on_delete=models.CASCADE, related_name='questoes')
    titulo_pergunta = models.CharField(max_length=250)
    tipo_pergunta = models.CharField(max_length=50, choices=TIPO_PERGUNTA_CHOICES, default='multipla escolha')
    obrigatoriedade = models.BooleanField()
    ordem = models.PositiveIntegerField(default=0) #para ordenar as questões no formulário
    
    class Meta:
        db_table = 'formulario_questao'
        ordering = ['ordem']
        
    def __str__(self):
        return f"{self.titulo_pergunta} ({self.get_tipo_pergunta_display()})"
    
    def clean(self):
        erros = {}
        if not self.titulo_pergunta or len(self.titulo_pergunta) < 5:
            erros['titulo_pergunta'] = "A pergunta deve ter um título com pelo menos 5 caracteres."
        if erros:
            raise ValidationError(erros)

class FormularioQuestaoOpcao(models.Model):
    questao = models.ForeignKey(FormularioQuestao, on_delete=models.CASCADE, related_name='opcoes')
    alternativa = models.CharField(max_length=250)

    class Meta:
        db_table = 'formulario_questao_opcao'
        ordering = ['id']

    def __str__(self):
        return f"{self.alternativa}"

    def clean(self):
        erros = {}
        if len(self.alternativa) < 1:
            erros['alternativa'] = "O enunciado da alternativa não pode estar vazio."
        #se a questao for de multipla escolha, deve ter opções
        if self.questao.tipo_pergunta in ['multipla escolha', 'caixas de selecao'] and not self.alternativa:
            erros['alternativa'] = "Questões de múltipla escolha devem ter alternativas definidas."
        if erros:
            raise ValidationError(erros)

class RespostaFormulario(models.Model):
    formulario = models.ForeignKey(Formulario, on_delete=models.CASCADE, related_name='respostas')
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE)
    data_resposta = models.DateTimeField(auto_now_add=True)
    completo = models.BooleanField(default=False) #coloquei pra indicar se o formulário foi completamente respondido pelo aluno

    class Meta:
        db_table = 'resposta_formulario'
        unique_together = ('formulario', 'aluno') #um aluno só pode responder um formulário específico uma única vez 

    def __str__(self):
        return f"Resposta de {self.aluno} para {self.formulario}"

    def clean(self):
        erros = {}
        #verificação se o aluno está apto a responder o formulário
        if self.formulario.solicitados != 'todos' and self.aluno.curso not in self.formulario.solicitados:
            erros['aluno'] = "Este aluno não está no grupo solicitado para este formulário."
        if erros:
            raise ValidationError(erros)

class RespostaQuestao(models.Model):
    resposta_formulario = models.ForeignKey(RespostaFormulario, on_delete=models.CASCADE, related_name='respostas_questoes')
    questao = models.ForeignKey(FormularioQuestao, on_delete=models.CASCADE)
    opcao_escolhida = models.ForeignKey(FormularioQuestaoOpcao, on_delete=models.SET_NULL, null=True, blank=True)
    resposta_aberta = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'resposta_questao'
        unique_together = ('resposta_formulario', 'questao') #para evitar respostas duplicadas para mesma questao

    def __str__(self):
        return f"Resposta para {self.questao}"

    def clean(self):
        erros = {}
        #validação baseada no tipo de pergunta
        if self.questao.tipo_pergunta in ['paragrafo'] and not self.resposta_aberta:
            erros['resposta_aberta'] = "Esta questão requer uma resposta textual."
            
        elif self.questao.tipo_pergunta in ['multipla escolha', 'caixas de selecao'] and not self.opcao_escolhida:
            erros['opcao_escolhida'] = "Esta questão requer uma seleção de opção."
        
        #validação da obrigatoriedade de resposta
        if self.questao.obrigatoriedade and not (self.opcao_escolhida or self.resposta_aberta):
            erros['opcao_escolhida'] = "Esta questão é obrigatória."
            erros['resposta_aberta'] = "Esta questão é obrigatória."
            
        if erros:
            raise ValidationError(erros)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
        
class Documento(models.Model):
    titulo = models.CharField(max_length=100, default='')
    tipo_documento = models.CharField(max_length=35, choices=TIPO_DOCUMENTO_CHOICES)
    descricao = models.CharField(max_length=100, null=True, blank=True)
    aluno = models.ForeignKey(
        'Aluno',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='documentos_criados'
    )
    assistente_social = models.ForeignKey(
        'AssistenteSocial',
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    solicitacao = models.ForeignKey(
        'Solicitacao',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='documentos'
    )

    # relatorio = models.ForeignKey(
    #     'Relatorio',
    #     null=True,
    #     blank=True,
    #     on_delete=models.CASCADE,
    #     related_name='documentos'
    # )

    data_criacao = models.DateTimeField(auto_now_add=True)
    arquivo = models.FileField(upload_to='documentos/', null=True, blank=True)

    class Meta:
        db_table = 'documento'

    def __str__(self):
        return f"Documento {self.id}"
        
class Pergunta(models.Model):
    enunciado = models.CharField(max_length=900)
    resposta = models.CharField(max_length=900, blank=True, null=True)
    status = models.CharField(max_length=100, choices=STATUS_PERGUNTA_CHOICES)
    data_realizacao = models.DateField(auto_now_add=True)
    data_resposta = models.DateField(null=True, blank=True)
    assistente_social = models.ForeignKey('AssistenteSocial', on_delete=models.SET_NULL, null=True, blank=True) 
    aluno = models.ForeignKey('Aluno', on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        db_table = 'pergunta'

    def __str__(self):
        return f"Pergunta #{self.id}"

    def clean(self):
        hoje = date.today()

        if self.data_realizacao and self.data_realizacao > hoje:
            raise ValidationError({'data_realizacao': 'Data de realização não pode ser futura.'})

        if self.data_resposta and self.data_resposta > hoje:
            raise ValidationError({'data_resposta': 'Data de resposta não pode ser futura.'})

        if self.data_realizacao and self.data_resposta:
            if self.data_realizacao > self.data_resposta:
                raise ValidationError({'data_resposta': 'Data de resposta não pode ser menor que a data de realização.'})
            
            if date.today() > self.data_resposta:
                raise ValidationError({'data_resposta': 'Data de resposta não pode ser no passado, tem que ser de hoje'})
            
        

class Notificacao(models.Model): 
    titulo = models.CharField(max_length=50, null=True, blank=True)
    data_envio = models.DateField(auto_now_add=True)
    mensagem = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_NOTIFICACAO_CHOICES)
    data_visualizacao = models.DateField(null=True, blank=True)
    usuario = models.ManyToManyField(Usuario, related_name="notificacoes")  
    tipo = models.CharField(max_length=20, choices=TIPO_NOTIFICACAO_CHOICES, default='geral')  # Adicionei o campo tipo

    class Meta:
        db_table = 'notificacao'

    def __str__(self):
        return f"Notificação #{self.id}" 
##coloquei o META pra ajudar os nomes das tabelas no banco fiquem iguaiss os que estão no dicionario de dadps, e coloquei o "def __str__(self):" pra ordenar e prdronizar melhor a exibção das notificações, por exemplo
##a quantidade de caracteres da matricula da assistente social é 7, e a quantidade de caracteres pra senha é 10, NO MÍNIMO.


class StatusSolicitacao(models.Model):
    codigo = models.IntegerField(unique=True)
    descricao = models.CharField(max_length=100)
    ordem = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'solicitacao_status'
        ordering = ['ordem']

    def __str__(self):
        return str(self.ordem)
    

class Solicitacao(models.Model):
    status = models.ForeignKey('StatusSolicitacao', on_delete=models.PROTECT, related_name = 'solicitacoes')
    descricao = models.CharField(max_length=200)
    data_criacao = models.DateField(auto_now_add=True)
    data_deferimento = models.DateField(null= True, blank = True)
    id_assistente_social = models.ForeignKey('AssistenteSocial', on_delete=models.CASCADE, related_name="id_AS", null= True, blank = True) # assistente social que deferiu ou nao deferiu o aluno
    id_aluno = models.ForeignKey('Aluno', on_delete=models.CASCADE, related_name="id_aluno")
    tipo_auxilio = models.ForeignKey('Auxilio', on_delete=models.CASCADE, related_name="auxilio")
    class Meta:
        db_table = "solicitacao"

    def clean(self):
        erros = {}

        # Regras de datas
        if self.data_criacao and self.data_deferimento and self.data_deferimento < self.data_criacao:
            erros['data_deferimento'] = "A data de deferimento não pode ser anterior à data de criação."

        if self.status.descricao == 'DEFERIDO' and not self.data_deferimento:
            erros['data_deferimento'] = "Deferimento exige data de deferimento"

        if self.status.descricao == 'EM_ANALISE' and self.data_deferimento:
            erros['status'] = "Status 'em análise' não deve ter data de deferimento"

        # Regras de benefício ativo
        aluno = self.id_aluno

        existe_deferimento_ativo = Beneficio.objects.filter(
            aluno=aluno,
            tipo_auxilio=self.tipo_auxilio,
            status=True   
        ).exclude(id=self.id if self.id else None)

        if existe_deferimento_ativo.exists():
            erros['status'] = "O aluno já possui um benefício ativo para este auxílio."

        if erros:
            raise ValidationError(erros)

    def __str__(self):
        return f"Solicitação {self.status}"


class Beneficio(models.Model):
    aluno = models.ForeignKey('Aluno', on_delete=models.CASCADE, related_name="beneficio")
    solicitacao = models.ForeignKey('Solicitacao', on_delete=models.CASCADE, related_name="beneficio")
    tipo_auxilio = models.ForeignKey('Auxilio', on_delete=models.CASCADE, related_name="beneficio")
    status = models.BooleanField(default=True)
    data_inicio = models.DateField(auto_now_add=True)
    data_fim = models.DateField()
    data_finalizacao = models.DateField(null=True, blank=True)
    justificativa_finalizacao = models.CharField(max_length=200, null=True, blank=True)

    def clean(self):
        erros = {}        
        if self.data_fim and self.data_inicio and self.data_inicio > self.data_fim:
            erros['data_fim'] = "A data de início não pode ser posterior à data de término."
        if self.data_finalizacao and self.data_inicio and self.data_finalizacao < self.data_inicio:
            erros['data_finalizacao'] = "A data de finalização não pode ser anterior à data de início."
        if erros:
            raise ValidationError(erros)

    def __str__(self):
        return self.tipo_auxilio.descricao
    
    class Meta:
        db_table = "beneficio"


class Auxilio(models.Model):
    nome = models.CharField(max_length=100, choices=TIPO_DE_AUXILIO, default="")
    campus = models.CharField(max_length=100, choices=CAMPUS_IFRN_CHOICES, default="")
    descricao = models.CharField(max_length=500, default="")
    qtd_chamados = models.IntegerField(blank=True, null=True, default=0)
    impedir_aluno = models.BooleanField(default=False)
    exigir_comprov = models.BooleanField(default=False)
    exigir_frequen = models.BooleanField(default=False)
    disponibilidade = models.BooleanField(default=False)
    edital = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.nome
    
    def clean(self):
        erros = {}
        if self.qtd_chamados is not None and self.qtd_chamados < 0:
            erros['qtd_chamados'] = "Quantidade de chamados não pode ser negativa"
        if self.disponibilidade:
            if not self.edital:
                erros['edital'] = "Auxílio disponível exige edital"
            if not self.exigir_frequen:
                erros['exigir_frequen'] = "Auxílio disponível exige frequência"

        if not self.disponibilidade:
            if self.exigir_frequen:
                erros['exigir_frequen'] = "Auxílio indisponível não exige frequência"
            if self.exigir_comprov:
                erros['exigir_comprov'] = "Auxílio indisponível não exige comprovante"
            if self.impedir_aluno:
                erros['impedir_aluno'] = "Auxílio indisponível não permite aluno solicitar"

        if erros:
            raise ValidationError(erros)

    class Meta:
        db_table = "auxilio"
        
class Chamado(models.Model):
    descricao = models.TextField()
    tipo_de_chamado = models.CharField(max_length=25, choices=TIPO_DE_CHAMADO_CHOICES, default="alteracao de documentos")
    tipo_de_auxilio = models.ForeignKey(Auxilio, on_delete=models.PROTECT, related_name="chamados", verbose_name="tipo de auxilio")
    status = models.CharField(max_length=10, choices=STATUS_CHAMADO_CHOICES, default="em_analise")
    data_abertura = models.DateField(auto_now_add=True)
    data_analise = models.DateField(auto_now=True)
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, verbose_name="chamados")
    assistente_social = models.ForeignKey(AssistenteSocial, on_delete=models.CASCADE, verbose_name="chamados") # não botei o on_delete na AS pra o chamado continuar se a AS for deletada
    documentos = models.ManyToManyField(Documento, verbose_name="documentos")
    justificativa_chamado = models.CharField(max_length=200, null=True, blank=True) # justificcativa para encerrar um chmado antes de concluis
    
    def __str__(self):
        return f"{self.id} - {self.descricao} - {self.aluno}"
    
    def clean(self):
        erros = {}
        if self.descricao == "":
            erros['descricao'] = "O chamado deve ter uma descrição"
        if erros:
            raise ValidationError(erros) 
    
    class Meta:
        db_table = 'chamado'

class Cursos(models.Model):
    nome = models.CharField(max_length=100, choices=CURSOS_IFRN_NATAL_CENTRAL, default="")

    def __str__(self):
        return self.nome

    class Meta:
        db_table = "cursos"


class Chamado_chat(models.Model):
    mensagem = models.TextField()
    lida = models.BooleanField(default=False)
    data_envio = models.DateTimeField(auto_now_add=True)
    data_leitura = models.DateTimeField(blank=True, null=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    chamado = models.ForeignKey(Chamado, on_delete=models.CASCADE, related_name="mensagens")
    arquivo = models.ForeignKey(Documento, on_delete=models.SET_NULL, null=True, blank=True)


    def clean(self):
        erros = {}
        if self.data_leitura and self.data_envio > self.data_leitura:
            erros['data_leitura'] = "A data de leitura não pode ser anterior à data de envio."
        if self.lida and not self.data_leitura:
            erros['data_leitura'] = "A data de leitura deve ser preenchida quando a mensagem for marcada como lida."
        if erros:   
            raise ValidationError(erros)    
    class Meta:
        db_table = 'chamado_chat'
        ordering = ['data_envio']