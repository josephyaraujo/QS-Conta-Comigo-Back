from django.test import TestCase
from api.tests.factories import criar_dados_solicitacao
from rest_framework.test import APIRequestFactory

from api.models import (
    AssistenteSocial,
    Usuario,
    Aluno,
    Auxilio,
    Solicitacao,
    StatusSolicitacao,
    Cursos,
)
from api.serializers.auxilio_beneficio import (
    SolicitacaoCreateSerializer,
    SolicitacaoSerializer,
    SolicitacaoDetailsSerializer,
)


class TestSolicitacaoSerializers(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()

        dados = criar_dados_solicitacao("Solicitação teste")
        for nome, valor in dados.items():
            setattr(self, nome, valor)

        self.status_inicial = StatusSolicitacao.objects.create(
            codigo=1,
            descricao="EM_ANALISE",
        )

    def test_solicitacao_create_serializer_cria_objeto_com_aluno_logado(self):
        request = self.factory.post("/solicitacoes/")
        request.user = self.usuario

        serializer = SolicitacaoCreateSerializer(
            data={
                "descricao": "Nova solicitação",
                "tipo_auxilio": self.tipo_auxilio.id,
            },
            context={"request": request},
        )

        self.assertTrue(serializer.is_valid(), serializer.errors)
        obj = serializer.save()

        self.assertEqual(obj.id_aluno_id, self.aluno.id)
        self.assertEqual(obj.status.codigo, 1)
        self.assertEqual(obj.descricao, "Nova solicitação")
        self.assertEqual(obj.tipo_auxilio_id, self.tipo_auxilio.id)

    def test_solicitacao_serializer_retorna_campos_esperados(self):
        data = SolicitacaoSerializer(instance=self.solicitacao).data

        self.assertIn("status", data)
        self.assertIn("descricao", data)
        self.assertIn("data_deferimento", data)
        self.assertIn("id_aluno", data)
        self.assertIn("data_criacao", data)
        self.assertIn("id_assistente_social", data)
        self.assertIn("tipo_auxilio", data)

    def test_solicitacao_details_serializer_retorna_dados_formatados(self):
        data = SolicitacaoDetailsSerializer(instance=self.solicitacao).data

        self.assertEqual(data["descricao"], "Solicitação teste")
        self.assertIn("id_aluno", data)
        self.assertIn("programa", data)
