from django.test import TestCase

from api.serializers.base import AssistenteSocialSerializer
from api.tests.factories import criar_dados_assistente_social


class TestAssistenteSocialSerializer(TestCase):
    def setUp(self):
        dados = criar_dados_assistente_social()
        self.usuario = dados["usuario"]
        self.assistente_social = dados["assistente_social"]

    def test_AS_serializer_leitura_retorna_campos_esperados(self):
        data = AssistenteSocialSerializer(instance=self.assistente_social).data
        self.assertIn("id", data)
        self.assertIn("usuario", data)
        self.assertIn("matricula", data)
