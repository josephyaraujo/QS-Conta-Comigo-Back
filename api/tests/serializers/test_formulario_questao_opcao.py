from django.test import TestCase

from api.serializers import FormularioQuestaoOpcaoSerializer
from api.tests.factories import criar_dados_formulario_questao


class TestFormularioQuestaoOpcaoSerializer(TestCase):
    def setUp(self):
        dados = criar_dados_formulario_questao(
            alternativa="Opção de teste",
        )
        for nome, valor in dados.items():
            setattr(self, nome, valor)

        self.opcao_data = {
            "questao": self.questao.id,
            "alternativa": "Opção de teste",
        }

    def test_serializer_com_dados_validos(self):
        serializer = FormularioQuestaoOpcaoSerializer(data=self.opcao_data)
        self.assertTrue(serializer.is_valid())

    def test_serializer_com_dados_invalidos_falta_alternativa(self):
        dados_invalidos = self.opcao_data.copy()
        dados_invalidos.pop("alternativa")
        serializer = FormularioQuestaoOpcaoSerializer(data=dados_invalidos)
        self.assertFalse(serializer.is_valid())
        self.assertIn("alternativa", serializer.errors)

    def test_serializer_com_dado_invalido_caracteres_maximos(self):
        dados_invalidos = self.opcao_data.copy()
        dados_invalidos["alternativa"] = "A" * 251
        serializer = FormularioQuestaoOpcaoSerializer(data=dados_invalidos)
        self.assertFalse(serializer.is_valid())
        self.assertIn("alternativa", serializer.errors)

    def test_serializer_contem_campos_esperados(self):
        serializer = FormularioQuestaoOpcaoSerializer(instance=self.opcao)
        data = serializer.data
        campos_esperados = {"id", "alternativa"}
        # Verifica se os campos gerados pelo serializer contêm pelo menos os campos base da opção
        self.assertTrue(campos_esperados.issubset(set(data.keys())))
