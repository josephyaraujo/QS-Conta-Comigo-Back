from datetime import date, timedelta
from api.tests.factories import criar_dados_formulario_questao
from django.core.exceptions import ValidationError
from django.test import TestCase
from api.models import Formulario, FormularioQuestao, FormularioQuestaoOpcao, Auxilio
from api.serializers.base import FormularioQuestaoOpcaoSimpleSerializer


class TestFormularioQuestaoOpcaoModel(TestCase):
    def setUp(self):
        dados = criar_dados_formulario_questao(
            titulo_pergunta="Qual a sua renda?",
            alternativa="A" * 250,
        )
        for nome, valor in dados.items():
            setattr(self, nome, valor)

    # ----- Testes alternativa Opção ----------
    def test_alternativa_opcao_caracteres_maximo_valido(self):
        field = FormularioQuestaoOpcao._meta.get_field("alternativa")
        self.assertEqual(field.max_length, 250)

    def test_alternativa_opcao_caracteres_superior_invalido(self):
        opcao = FormularioQuestaoOpcao(questao=self.questao, alternativa="A" * 251)
        with self.assertRaises(ValidationError):
            opcao.full_clean()

    def test_alternativa_opcao_vazio_invalido(self):
        opcao = FormularioQuestaoOpcao(questao=self.questao, alternativa="")
        with self.assertRaises(ValidationError):
            opcao.full_clean()


class TestFormularioQuestaoOpcaoSimpleSerializer(TestCase):
    def setUp(self):
        dados = criar_dados_formulario_questao(
            alternativa="Opção de teste",
        )
        for nome, valor in dados.items():
            setattr(self, nome, valor)

        self.opcao_data = {"alternativa": "Opção de teste"}

    def test_serializer_com_dados_validos(self):
        serializer = FormularioQuestaoOpcaoSimpleSerializer(data=self.opcao_data)
        self.assertTrue(serializer.is_valid())

    def test_serializer_com_dados_invalidos_falta_alternativa(self):
        dados_invalidos = self.opcao_data.copy()
        dados_invalidos.pop("alternativa")
        serializer = FormularioQuestaoOpcaoSimpleSerializer(data=dados_invalidos)
        self.assertFalse(serializer.is_valid())
        self.assertIn("alternativa", serializer.errors)

    def test_serializer_com_dado_invalido_caracteres_maximos(self):
        dados_invalidos = self.opcao_data.copy()
        dados_invalidos["alternativa"] = "A" * 251
        serializer = FormularioQuestaoOpcaoSimpleSerializer(data=dados_invalidos)
        self.assertFalse(serializer.is_valid())
        self.assertIn("alternativa", serializer.errors)

    def test_serializer_contem_campos_esperados(self):
        serializer = FormularioQuestaoOpcaoSimpleSerializer(instance=self.opcao)
        data = serializer.data
        campos_esperados = {"id", "alternativa"}
        self.assertTrue(campos_esperados.issubset(set(data.keys())))
