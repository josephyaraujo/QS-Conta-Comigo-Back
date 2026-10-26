from datetime import date, timedelta

from django.core.exceptions import ValidationError
from django.test import TestCase

from api.models import FormularioQuestao
from api.tests.factories import criar_dados_formulario_questao


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


