from django.test import TestCase
from datetime import date, timedelta

from api.models import Beneficio, AssistenteSocial, Usuario, Aluno, Auxilio, Solicitacao, StatusSolicitacao, Cursos
from api.serializers.auxilio_beneficio import (
    BeneficioCreateSerializer,
    BeneficioSerializer,
    BeneficioAlunoSerializer,
)

class TestBeneficioSerializers(TestCase):
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
            data_inicio = date.today(),
            data_fim = date.today() + timedelta(days=30),
            data_finalizacao = date.today() + timedelta(days=30),
            justificativa_finalizacao = 'B' * 200
        )
    
    def test_beneficio_create_serializer_valida_dados_corretos(self):
        serializer = BeneficioCreateSerializer(
            data={
                "aluno_id": self.aluno.id,
                "solicitacao_id": self.solicitacao.id,
                "tipo_auxilio": self.tipo_auxilio.id,
                "status": True,
                "data_fim": date.today() + timedelta(days=30),
                "data_finalizacao": date.today() + timedelta(days=30),
                "justificativa_finalizacao": 'B' * 200,
                "data_inicio": date.today()
            }
        )
        self.assertTrue(serializer.is_valid())

    def test_beneficio_serializer_retorna_campos_esperados(self):
        data = BeneficioSerializer(instance=self.beneficio).data

        self.assertIn("aluno", data)
        self.assertIn("tipo_auxilio", data)
        self.assertIn("status", data)
        self.assertIn("data_fim", data)
        self.assertIn("data_finalizacao", data)
        self.assertIn("data_inicio", data)
        self.assertIn("justificativa_finalizacao", data)
        self.assertIn("motivo_entrada", data)
        self.assertIn("parecer", data)
    
    def test_beneficio_aluno_serializer_retorna_campos_esperados(self):
        data = BeneficioAlunoSerializer(instance=self.beneficio).data

        self.assertIn("id", data)
        self.assertIn("status", data)
        self.assertIn("titulo", data)
        self.assertIn("data_inicio", data)