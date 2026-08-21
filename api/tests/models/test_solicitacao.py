from datetime import date, timedelta
from django.core.exceptions import ValidationError
from api.models import AssistenteSocial, Usuario, Cursos, Beneficio, Aluno, Solicitacao, Auxilio, StatusSolicitacao
from django.test import TestCase

class TestSolicitacaoModel(TestCase):
    def setUp(self):
        self.usuario = Usuario.objects.create(nome_completo = 'Pafinha Silva', email = 'pafinhaSilva@gmail.com')
        self.statusSolicitacao = StatusSolicitacao.objects.create(codigo = 44, descricao = 'A' * 100)
        self.curso = Cursos.objects.create(nome = 'Tecnologia em Análise e Desenvolvimento de Sistemas')
        self.aluno = Aluno.objects.create(
            usuario = self.usuario,
            matricula = '20241014040025',
            cpf = '55284158024',
            curso = self.curso,
            periodo = 4,
            status = 'Matriculado no SUAP',
            campus = 'Natal-Central',
            ingresso = None,
            qtd_periodos = 6
        )
        self.assistente_social = AssistenteSocial.objects.create(
            usuario = self.usuario,
            matricula = '2024101'
        )
        self.tipo_auxilio = Auxilio.objects.create()   
        self.solicitacao = Solicitacao.objects.create(
            status = self.statusSolicitacao,
            descricao = 'B' * 200,
            id_assistente_social = self.assistente_social,
            id_aluno = self.aluno,
            tipo_auxilio = self.tipo_auxilio
        )
    
    def test_descricao_abaixo_do_limite_valida(self):
        field = Solicitacao._meta.get_field('descricao')
        self.assertEqual(field.max_length, 200)
    
    def test_descricao_acima_do_limite_invalida(self):
        solicitacao = Solicitacao(
            status = self.statusSolicitacao,
            descricao = 'B' * 201,
            id_assistente_social = self.assistente_social,
            id_aluno = self.aluno,
            tipo_auxilio = self.tipo_auxilio
        )
        with self.assertRaises(ValidationError):
            solicitacao.full_clean()

    def test_data_deferimento_menor_que_data_criacao_invalida(self):
        solicitacao = Solicitacao(
            status = self.statusSolicitacao,
            descricao = 'B' * 200,
            id_assistente_social = self.assistente_social,
            id_aluno = self.aluno,
            tipo_auxilio = self.tipo_auxilio,
            data_criacao = date.today(),
            data_deferimento = date.today() - timedelta(days=1)
        )
        with self.assertRaises(ValidationError) as ctx:
            solicitacao.full_clean()

        self.assertIn('data_deferimento', ctx.exception.message_dict)

    def test_data_deferimento_igual_data_criacao_valida(self):
        solicitacao = Solicitacao(
            status = self.statusSolicitacao,
            descricao = 'B' * 200,
            id_assistente_social = self.assistente_social,
            id_aluno = self.aluno,
            tipo_auxilio = self.tipo_auxilio,
            data_criacao = date.today(),
            data_deferimento = date.today()
        )
        try:
            solicitacao.full_clean()
        except ValidationError:
            self.fail('Solicitação com data de deferimento igual à data de criação deve ser válida.')
    
    def test_data_deferimento_maior_que_data_criacao_valida(self):
        solicitacao = Solicitacao(
            status = self.statusSolicitacao,
            descricao = 'B' * 200,
            id_assistente_social = self.assistente_social,
            id_aluno = self.aluno,
            tipo_auxilio = self.tipo_auxilio,
            data_criacao = date.today(),
            data_deferimento = date.today() + timedelta(days=1)
        )
        try:
            solicitacao.full_clean()
        except ValidationError:
            self.fail('Solicitação com data de deferimento maior que a data de criação deve ser válida.')

    def test_codigo_deferido_exige_data_deferimento_valida(self):
        solicitacao = Solicitacao(
            descricao = 'B' * 200,
            id_assistente_social = self.assistente_social,
            id_aluno = self.aluno,
            tipo_auxilio = self.tipo_auxilio,
            data_criacao = date.today(),
            data_deferimento = date.today() + timedelta(days=1),
            status = StatusSolicitacao.objects.create(codigo=45, descricao='DEFERIDO')  
        )   

        try:
            solicitacao.full_clean()
        except ValidationError:
            self.fail('Solicitação com status "DEFERIDO" e data de deferimento deve ser válida.')

    def test_codigo_deferido_sem_data_deferimento_invalida(self):
        solicitacao = Solicitacao(
            descricao = 'B' * 200,
            id_assistente_social = self.assistente_social,
            id_aluno = self.aluno,
            tipo_auxilio = self.tipo_auxilio,
            data_criacao = date.today(),
            status = StatusSolicitacao.objects.create(codigo=45, descricao='DEFERIDO')
        )

        with self.assertRaises(ValidationError) as ctx:
            solicitacao.full_clean()

        self.assertIn('data_deferimento', ctx.exception.message_dict)
    
    def test_codigo_analise_sem_data_deferimento_valida(self):
        solicitacao = Solicitacao(
            descricao = 'B' * 200,
            id_assistente_social = self.assistente_social,
            id_aluno = self.aluno,
            tipo_auxilio = self.tipo_auxilio,
            data_criacao = date.today(),
            status = StatusSolicitacao.objects.create(codigo=46, descricao='EM_ANALISE')
        )   

        try:
            solicitacao.full_clean() 
        except ValidationError:
            self.fail('Solicitação com status "EM_ANALISE" sem data de deferimento deve ser válida.')
    
    def test_codigo_analise_com_data_deferimento_invalida(self):
        solicitacao = Solicitacao(
            descricao = 'B' * 200,
            id_assistente_social = self.assistente_social,
            id_aluno = self.aluno,
            tipo_auxilio = self.tipo_auxilio,
            data_criacao = date.today(),
            data_deferimento = date.today() + timedelta(days=1),
            status = StatusSolicitacao.objects.create(codigo=46, descricao='EM_ANALISE')
        )   

        with self.assertRaises(ValidationError) as ctx:
            solicitacao.full_clean()

        self.assertIn('status', ctx.exception.message_dict)
    
    #teste de beneficio ativo nao sei fazer
