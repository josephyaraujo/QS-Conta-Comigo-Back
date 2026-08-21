from datetime import date, timedelta
from django.core.exceptions import ValidationError
from api.models import AssistenteSocial, Usuario, Cursos, Beneficio, Aluno, Solicitacao, Auxilio, StatusSolicitacao
from django.test import TestCase

class TestBeneficioModel(TestCase):
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
            descricao = 'B' * 100,
            id_assistente_social = self.assistente_social,
            id_aluno = self.aluno,
            tipo_auxilio = self.tipo_auxilio
        )
        self.beneficio = Beneficio.objects.create(
            aluno = self.aluno,
            solicitacao = self.solicitacao,
            tipo_auxilio = self.tipo_auxilio,
            status = True,
            data_fim = date.today() + timedelta(days=30),
            data_finalizacao = date.today() + timedelta(days=30),
            justificativa_finalizacao = 'B' * 200
        )

    def test_justificativa_abaixo_do_limite_valida(self):
        field = Beneficio._meta.get_field('justificativa_finalizacao')
        self.assertEqual(field.max_length, 200)
    
    def test_justificativa_acima_do_limite_invalida(self):
        beneficio = Beneficio(
            aluno = self.aluno,
            solicitacao = self.solicitacao,
            tipo_auxilio = self.tipo_auxilio,
            status = True,
            data_fim = date.today() + timedelta(days=30),
            data_finalizacao = date.today() + timedelta(days=30),
            justificativa_finalizacao = 'B' * 201
        )
        with self.assertRaises(ValidationError):
            beneficio.full_clean() 

    def test_data_fim_igual_data_inicio_valida(self):
        beneficio = Beneficio(
            aluno = self.aluno,
            solicitacao = self.solicitacao,
            tipo_auxilio = self.tipo_auxilio,
            status = True,
            data_fim = date.today(),
            data_finalizacao = date.today(),
            justificativa_finalizacao = 'B' * 200
        )
        try:
            beneficio.full_clean()
        except ValidationError:
            self.fail('Benefício com data_fim igual a data_inicio deve ser válido.')
            
    def test_data_fim_menor_que_data_inicio_invalida(self):
        beneficio = Beneficio(
            aluno = self.aluno,
            solicitacao = self.solicitacao,
            tipo_auxilio = self.tipo_auxilio,
            status = True,
            data_inicio = date.today(),
            data_fim = date.today() - timedelta(days=1),
            data_finalizacao = date.today() + timedelta(days=30),
            justificativa_finalizacao = 'B' * 200
        )
        with self.assertRaises(ValidationError) as ctx:
            beneficio.full_clean()
        
        self.assertIn('data_fim', ctx.exception.message_dict)

    def test_data_finalizacao_igual_data_inicio_valida(self):
        beneficio = Beneficio(
            aluno = self.aluno,
            solicitacao = self.solicitacao,
            tipo_auxilio = self.tipo_auxilio,
            status = True,
            data_fim = date.today() + timedelta(days=30),
            data_finalizacao = date.today(),
            justificativa_finalizacao = 'B' * 200
        )
        try:
            beneficio.full_clean()
        except ValidationError:
            self.fail('Benefício com data_finalizacao igual a data_inicio deve ser válido.')

    def test_data_finalizacao_menor_que_data_inicio_invalida(self):
        beneficio = Beneficio(
            aluno = self.aluno,
            solicitacao = self.solicitacao,
            tipo_auxilio = self.tipo_auxilio,
            status = True,
            data_inicio = date.today(),
            data_fim = date.today() + timedelta(days=30),
            data_finalizacao = date.today() - timedelta(days=1),
            justificativa_finalizacao = 'B' * 200
        )
        with self.assertRaises(ValidationError) as ctx:
            beneficio.full_clean()
        
        self.assertIn('data_finalizacao', ctx.exception.message_dict)


    