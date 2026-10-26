from datetime import date

from django.test import TestCase

from api.models import AssistenteSocial
from api.serializers.perguntas import (
    PerguntaRespostaSerializer,
    PerguntaSerializer,
)
from api.tests.factories import criar_dados_pergunta


class TestPerguntaSerializer(TestCase):
    def setUp(self):
        dados = criar_dados_pergunta()
        for nome, valor in dados.items():
            setattr(self, nome, valor)

        self.assistente_social = self.usuario.assistentesocial
        
        self.resposta = {
            "enunciado": self.pergunta.enunciado,
            "resposta": "resposta teste",
            "status": "respondida",
            "assistente_social": self.assistente_social.id,
        }

    def test_pergunta_serializer_retorna_campos_esperados_quando_nao_respondida(self):
        data = PerguntaSerializer(instance=self.pergunta).data
        self.assertIn("id", data)
        self.assertIn("enunciado", data)
        self.assertIn("resposta", data)
        self.assertIn("status", data)
        self.assertIn("data_realizacao", data)
        self.assertIn("data_resposta", data)
        self.assertIn("assistente_social", data)
        self.assertIn("aluno", data)

    def test_pergunta_resposta_serializer_retorna_campos_esperados(self):
        data = PerguntaRespostaSerializer(instance=self.pergunta).data
        self.assertIn("id", data)
        self.assertIn("resposta", data)
        self.assertIn("enunciado", data)
        self.assertIn("status", data)
        self.assertIn("assistente_social", data)

    def test_pergunta_resposta_serializer_valida_qtd_caracteres_resposta(
        self,
    ):  # coloquei aqui ao invés de no model porque nao é algo de create, mas sim de update, confirmar com marilia se isso faz sentido
        resposta_invalida = "A" * 901
        serializer = PerguntaRespostaSerializer(
            data={
                "enunciado": self.resposta["enunciado"],
                "resposta": resposta_invalida,
                "status": self.resposta["status"],
                "assistente_social": self.resposta["assistente_social"],
            }
        )
        self.assertFalse(serializer.is_valid())

    def test_pergunta_serializer_retorna_campos_esperados_quando_respondida(self):
        self.pergunta.resposta = "A" * 900
        self.pergunta.status = "respondida"
        self.pergunta.assistente_social = self.assistente_social
        data = PerguntaSerializer(instance=self.pergunta).data
        self.assertIn("id", data)
        self.assertIn("enunciado", data)
        self.assertIn("resposta", data)
        self.assertIn("status", data)
        self.assertIn("assistente_social", data)
