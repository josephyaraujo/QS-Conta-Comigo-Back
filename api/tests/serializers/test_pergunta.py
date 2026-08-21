from api.models import Aluno, AssistenteSocial, Cursos, Pergunta, Usuario
from api.serializers.perguntas import (PerguntaRespostaSerializer, PerguntaSerializer)
from django.test import TestCase
from datetime import date


class TestPerguntaSerializer(TestCase):
    def setUp(self):
        self.usuario = Usuario.objects.create(nome_completo = 'Usuario Teste', email = 'userteste@gmail.com')
        self.curso = Cursos.objects.create(nome = 'Tecnologia em Análise e Desenvolvimento de Sistemas')
        self.aluno = Aluno.objects.create(
            usuario = self.usuario,
            matricula = '20241014040025',
            cpf = '00000000000',
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
        self.pergunta = Pergunta.objects.create(
            enunciado = 'A' * 900,
            resposta = None,
            status = 'nao_respondida',
            data_realizacao =  date.today(),
            data_resposta = date.today(),
            assistente_social=None,
            aluno = self.aluno
        )
        self.resposta = {
            'enunciado': self.pergunta.enunciado,
            'resposta': 'resposta teste',
            'status': 'respondida',
            'assistente_social': self.assistente_social.id
        }
    
    def test_pergunta_serializer_retorna_campos_esperados_quando_nao_respondida(self):
        data = PerguntaSerializer(instance = self.pergunta).data
        self.assertIn('id', data)
        self.assertIn('enunciado', data)
        self.assertIn('resposta', data)
        self.assertIn('status', data)
        self.assertIn('data_realizacao', data)
        self.assertIn('data_resposta', data)
        self.assertIn('assistente_social', data)
        self.assertIn('aluno', data)

    def test_pergunta_resposta_serializer_retorna_campos_esperados(self):
        data = PerguntaRespostaSerializer(instance = self.pergunta).data
        self.assertIn('id', data)
        self.assertIn('resposta', data)
        self.assertIn('enunciado', data)
        self.assertIn('status', data)
        self.assertIn('assistente_social', data)

    def test_pergunta_resposta_serializer_valida_qtd_caracteres_resposta(self): # coloquei aqui ao invés de no model porque nao é algo de create, mas sim de update, confirmar com marilia se isso faz sentido
        resposta_invalida = 'A' * 901
        serializer = PerguntaRespostaSerializer(data={
            'enunciado': self.resposta['enunciado'],
            'resposta': resposta_invalida,
            'status': self.resposta['status'],
            'assistente_social': self.resposta['assistente_social']
        })
        self.assertFalse(serializer.is_valid())

    def test_pergunta_serializer_retorna_campos_esperados_quando_respondida(self):
        self.pergunta.resposta = 'A' * 900
        self.pergunta.status = 'respondida'
        self.pergunta.assistente_social = self.assistente_social
        data = PerguntaSerializer(instance=self.pergunta).data
        self.assertIn('id', data)
        self.assertIn('enunciado', data)
        self.assertIn('resposta', data)
        self.assertIn('status', data)
        self.assertIn('assistente_social', data)