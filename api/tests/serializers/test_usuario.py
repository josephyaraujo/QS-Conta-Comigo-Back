from django.test import TestCase

from api.serializers.base import UsuarioAuthSerializer, UsuarioSerializer
from api.tests.factories import criar_dados_aluno


class TestUsuarioSerializer(TestCase):
    def setUp(self):
        dados = criar_dados_aluno(
            nome_completo="Assistente Social Teste",
            email="usertest@gmail.com",
            criar_assistente_social=True,
        )
        self.usuario = dados["usuario"]
        self.aluno = dados["aluno"]
        self.assistente_social = dados["assistente_social"]

    def test_usuario_serializer_leitura_retorna_campos_esperados(self):
        data = UsuarioSerializer(instance=self.usuario).data
        self.assertIn("id", data)
        self.assertIn("nome_completo", data)

    def test_usuario_auth_serializer_AS_leitura_retorna_campos_esperados(self):
        usuario_data = {
            "usuario": self.usuario,
            "matricula": self.assistente_social.matricula,
            "tipo_usuario": "assistente social",
        }
        data = UsuarioAuthSerializer(instance=usuario_data).data
        self.assertIn("usuario", data)
        self.assertIn("matricula", data)
        self.assertIn("tipo_usuario", data)

    def test_usuario_auth_serializer_aluno_leitura_retorna_campos_esperados(self):
        usuario_data = {
            "usuario": self.usuario,
            "matricula": self.aluno.matricula,
            "tipo_usuario": "aluno",
        }
        data = UsuarioAuthSerializer(instance=usuario_data).data
        self.assertIn("usuario", data)
        self.assertIn("matricula", data)
        self.assertIn("tipo_usuario", data)
