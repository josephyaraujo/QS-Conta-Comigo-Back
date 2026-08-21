from api.models import Aluno, Cursos, Usuario
from api.serializers.base import (AlunoPerfilSerializer, AlunoSerializer, AlunoSimpleSerializer, AlunoReadOnlySerializer)
from django.test import TestCase
from datetime import date


class TestAlunoSerializer(TestCase):
    def setUp(self):
        self.usuario = Usuario.objects.create(nome_completo = 'Usuario Teste', email = 'userteste@gmail.com')
        self.curso = Cursos.objects.create(nome = 'Tecnologia em Análise e Desenvolvimento de Sistemas')
        self.aluno = Aluno.objects.create(
            usuario = self.usuario,
            matricula = '0' * 14,
            cpf = '0' * 11,
            curso = self.curso,
            periodo = 4,
            status = 'Matriculado no SUAP',
            campus = 'Natal-Central',
            ingresso = None,
            qtd_periodos = 6
        )
    
    def test_aluno_serializer_leitura_retorna_campos_esperados(self):
        data = AlunoReadOnlySerializer(instance = self.aluno).data
        self.assertIn('nome_completo', data)
        self.assertIn('matricula', data)
        self.assertIn('curso', data)

    def test_aluno_serializer_leitura_simple_retorna_campos_esperados(self):
        data = AlunoSimpleSerializer(instance = self.aluno).data
        self.assertIn('id', data)
        self.assertIn('nome', data)
        self.assertIn('matricula', data)

    def test_aluno_serializer_leitura_simple_retorna_campos_esperados(self):
        data = AlunoPerfilSerializer(instance = self.aluno).data
        self.assertIn('id', data)
        self.assertIn('usuario', data)
        self.assertIn('matricula', data)
        self.assertIn('cpf', data)
        self.assertIn('curso', data)
        self.assertIn('periodo', data)
        self.assertIn('status', data)
        self.assertIn('campus', data)
        self.assertIn('ingresso', data)
        self.assertIn('qtd_periodos', data)

    def test_aluno_serializer_retorna_campos_esperados(self):
        data = AlunoSerializer(instance = self.aluno).data
        self.assertIn('id',data)
        self.assertIn('full_name',data)
        self.assertIn('matricula',data)
        self.assertIn('cpf',data)
        self.assertIn('curso',data)
        self.assertIn('periodo',data)
        self.assertIn('status',data)
        self.assertIn('campus',data)
        self.assertIn('ingresso',data)
        self.assertIn('qtd_periodos',data)
        self.assertIn('documentos',data)


    