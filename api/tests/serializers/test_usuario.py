from api.models import  Aluno, AssistenteSocial, Cursos, Usuario
from api.serializers.base import (UsuarioAuthSerializer, UsuarioSerializer)
from django.test import TestCase

class TestUsuarioSerializer(TestCase):
    def setUp(self):
        self.usuario = Usuario.objects.create(nome_completo = 'Assistente Social Teste', email = 'usertest@gmail.com')
        self.aluno = Aluno.objects.create(
            usuario = self.usuario,
            matricula = '0' * 14,
            cpf = '0' * 11,
            curso = Cursos.objects.create(nome = 'Tecnologia em Análise e Desenvolvimento de Sistemas'),
            periodo = 4,
            status = 'Matriculado no SUAP',
            campus = 'Natal-Central',
            ingresso = None,
            qtd_periodos = 6
        )
        self.assistente_social = AssistenteSocial.objects.create(
            usuario = self.usuario,
            matricula = '0' * 7,
        )

    def test_usuario_serializer_leitura_retorna_campos_esperados(self):
        data = UsuarioSerializer(instance = self.usuario).data
        self.assertIn('id', data)
        self.assertIn('nome_completo', data)

    def test_usuario_auth_serializer_AS_leitura_retorna_campos_esperados(self):
        usuario_data = {
            'usuario': self.usuario,
            'matricula': self.assistente_social.matricula,
            'tipo_usuario': 'assistente social'
        }
        data = UsuarioAuthSerializer(instance = usuario_data).data
        self.assertIn('usuario', data)
        self.assertIn('matricula', data)
        self.assertIn('tipo_usuario', data)

    def test_usuario_auth_serializer_aluno_leitura_retorna_campos_esperados(self):
        usuario_data = {
            'usuario': self.usuario,
            'matricula': self.aluno.matricula,
            'tipo_usuario': 'aluno'
        }
        data = UsuarioAuthSerializer(instance = usuario_data).data
        self.assertIn('usuario', data)
        self.assertIn('matricula', data)
        self.assertIn('tipo_usuario', data)
