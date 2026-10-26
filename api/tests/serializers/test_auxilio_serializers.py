from django.test import TestCase

from api.models import Auxilio
from api.serializers.auxilio_beneficio import AuxilioListSerializer, AuxilioSerializer

from api.tests.factories import criar_dados_auxilio


class AuxilioSerializerTestCase(TestCase):
    def setUp(self):
        self.auxilio = Auxilio.objects.create(
            **criar_dados_auxilio(
                descricao="Auxílio para testes",
                qtd_chamados=2,
            )
        )

    def test_deve_serializar_todos_os_campos_esperados(self):
        serializer = AuxilioSerializer(instance=self.auxilio)
        data = serializer.data

        self.assertIn("id", data)
        self.assertIn("nome", data)
        self.assertIn("descricao", data)
        self.assertIn("campus", data)
        self.assertIn("qtd_participantes", data)
        self.assertIn("qtd_chamados", data)
        self.assertIn("impedir_aluno", data)
        self.assertIn("exigir_comprov", data)
        self.assertIn("exigir_frequen", data)
        self.assertIn("disponibilidade", data)
        self.assertIn("edital", data)

    def test_qtd_participantes_deve_ser_zero_quando_nao_ha_beneficios(self):
        serializer = AuxilioSerializer(instance=self.auxilio)

        self.assertEqual(serializer.data["qtd_participantes"], 0)

    def test_deve_validar_dados_para_criacao(self):
        payload = criar_dados_auxilio(
            descricao="Novo auxílio",
            qtd_chamados=1,
        )

        serializer = AuxilioSerializer(data=payload)

        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_deve_criar_auxilio_via_serializer(self):
        payload = criar_dados_auxilio(
            descricao="Auxílio criado via serializer",
            qtd_chamados=3,
        )

        serializer = AuxilioSerializer(data=payload)
        self.assertTrue(serializer.is_valid(), serializer.errors)

        auxilio = serializer.save()

        self.assertIsNotNone(auxilio.id)
        self.assertEqual(auxilio.descricao, "Auxílio criado via serializer")


class AuxilioListSerializerTestCase(TestCase):
    def setUp(self):
        self.auxilio = Auxilio.objects.create(
            **criar_dados_auxilio(
                descricao="Auxílio para listagem",
                qtd_chamados=0,
            )
        )

    def test_deve_serializar_apenas_id_e_nome(self):
        serializer = AuxilioListSerializer(instance=self.auxilio)
        data = serializer.data

        self.assertEqual(set(data.keys()), {"id", "nome"})

    def test_deve_serializar_lista_de_auxilios(self):
        serializer = AuxilioListSerializer(instance=[self.auxilio], many=True)

        self.assertEqual(len(serializer.data), 1)
        self.assertEqual(set(serializer.data[0].keys()), {"id", "nome"})
