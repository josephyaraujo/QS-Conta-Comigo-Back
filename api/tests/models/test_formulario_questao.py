from datetime import date, timedelta
from api.tests.factories import criar_dados_formulario_questao
from django.core.exceptions import ValidationError
from datetime import date, timedelta
from django.test import TestCase
from api.models import Formulario, FormularioQuestao, Auxilio
from api.serializers.base import FormularioQuestaoSimpleSerializer


class TestFormularioQuestaoModel(TestCase):
    def setUp(self):
        dados = criar_dados_formulario_questao(titulo_pergunta="A" * 250)
        for nome, valor in dados.items():
            setattr(self, nome, valor)

    # ----- Testes Titulo Pergunta ----------
    def test_titulo_pergunta_caracteres_maximo_valido(self):
        field = FormularioQuestao._meta.get_field("titulo_pergunta")
        self.assertEqual(field.max_length, 250)

    def test_titulo_pergunta_caracteres_superior_invalido(self):
        questao = FormularioQuestao(
            formulario=self.formulario,
            titulo_pergunta="A" * 251,
            tipo_pergunta="multipla escolha",
            obrigatoriedade=True,
        )
        with self.assertRaises(ValidationError):
            questao.full_clean()

    def test_titulo_pergunta_vazio_invalido(self):
        questao = FormularioQuestao(
            formulario=self.formulario,
            titulo_pergunta="",
            tipo_pergunta="multipla escolha",
            obrigatoriedade=True,
        )
        with self.assertRaises(ValidationError):
            questao.full_clean()


class TestFormularioQuestaoSimpleSerializer(TestCase):
    def setUp(self):
        dados = criar_dados_formulario_questao()
        for nome, valor in dados.items():
            setattr(self, nome, valor)

        self.questao_data = {
            "formulario": self.formulario.id,
            "titulo_pergunta": "Qual a sua renda familiar parcial?",
            "tipo_pergunta": "multipla_escolha",
            "obrigatoriedade": True,
        }

    def test_serializer_com_dados_validos(self):
        serializer = FormularioQuestaoSimpleSerializer(data=self.questao_data)
        eh_valido = serializer.is_valid()
        self.assertTrue(
            eh_valido, msg=f"O serializer rejeitou os dados. Erros: {serializer.errors}"
        )

    def test_serializer_com_dados_invalidos_falta_titulo(self):
        dados_invalidos = self.questao_data.copy()
        dados_invalidos.pop("titulo_pergunta")
        serializer = FormularioQuestaoSimpleSerializer(data=dados_invalidos)
        self.assertFalse(serializer.is_valid())
        self.assertIn("titulo_pergunta", serializer.errors)

    def test_serializer_com_dado_invalido_caracteres_maximos(self):
        dados_invalidos = self.questao_data.copy()
        dados_invalidos["titulo_pergunta"] = "A" * 251
        serializer = FormularioQuestaoSimpleSerializer(data=dados_invalidos)
        self.assertFalse(serializer.is_valid())
        self.assertIn("titulo_pergunta", serializer.errors)

    def test_serializer_contem_campos_esperados(self):
        serializer = FormularioQuestaoSimpleSerializer(instance=self.questao)
        data = serializer.data
        campos_esperados = {"id", "titulo_pergunta", "tipo_pergunta", "obrigatoriedade"}
        self.assertTrue(campos_esperados.issubset(set(data.keys())))
