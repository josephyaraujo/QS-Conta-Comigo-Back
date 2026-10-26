from datetime import date

from django.test import TestCase

from api.serializers.base import (
    AlunoPerfilSerializer,
    AlunoSerializer,
    AlunoSimpleSerializer,
    AlunoReadOnlySerializer,
)
from api.tests.factories import criar_dados_aluno


class TestAlunoSerializer(TestCase):
    def setUp(self):
        dados = criar_dados_aluno()
        self.usuario = dados["usuario"]
        self.curso = dados["curso"]
        self.aluno = dados["aluno"]

    def test_aluno_serializer_leitura_retorna_campos_esperados(self):
        data = AlunoReadOnlySerializer(instance=self.aluno).data
        self.assertIn("nome_completo", data)
        self.assertIn("matricula", data)
        self.assertIn("curso", data)

    def test_aluno_serializer_leitura_simple_retorna_campos_esperados(self):
        data = AlunoSimpleSerializer(instance=self.aluno).data
        self.assertIn("id", data)
        self.assertIn("nome", data)
        self.assertIn("matricula", data)

    def test_aluno_serializer_leitura_simple_retorna_campos_esperados(self):
        data = AlunoPerfilSerializer(instance=self.aluno).data
        self.assertIn("id", data)
        self.assertIn("usuario", data)
        self.assertIn("matricula", data)
        self.assertIn("cpf", data)
        self.assertIn("curso", data)
        self.assertIn("periodo", data)
        self.assertIn("status", data)
        self.assertIn("campus", data)
        self.assertIn("ingresso", data)
        self.assertIn("qtd_periodos", data)

    def test_aluno_serializer_retorna_campos_esperados(self):
        data = AlunoSerializer(instance=self.aluno).data
        self.assertIn("id", data)
        self.assertIn("full_name", data)
        self.assertIn("matricula", data)
        self.assertIn("cpf", data)
        self.assertIn("curso", data)
        self.assertIn("periodo", data)
        self.assertIn("status", data)
        self.assertIn("campus", data)
        self.assertIn("ingresso", data)
        self.assertIn("qtd_periodos", data)
        self.assertIn("documentos", data)
